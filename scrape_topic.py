import re

import click
from tqdm import tqdm

import config
import jsonlines
import vk_api

import os

vk_session = vk_api.VkApi(app_id=config.APP_ID, token=config.TOKEN)
vk = vk_session.get_api()


os.makedirs('data', exist_ok=True)


@click.command()
@click.option('--topic_url', '-t', help='VK group topic url')
def main(topic_url):
    match = re.search('topic-(\d+)_(\d+)', topic_url)
    group_id = match.group(1)
    topic_id = match.group(2)


    count = 0
    per_page = 100

    # https://vk.com/dev/board.getComments
    comments = vk.board.getComments(group_id=group_id, topic_id=topic_id, need_likes=1, count=per_page)
    total_count = comments['count']

    all_comments = []

    writer = jsonlines.open('data/{}-{}.jsonl'.format(group_id, topic_id), mode='w')

    for i in tqdm(range(total_count//per_page)):
        res = vk.board.getComments(group_id=group_id, topic_id=topic_id, need_likes=1, offset=i*per_page, count=per_page, extended=1)
        all_comments.append(res['items'])
        writer.write_all(res['items'])


if __name__ == '__main__':
    main()

