"""
Functions added to handle data coming from raw sql queries.
"""

def idea_to_json(idea):
    json = dict(
        idea_id=idea.idea_id,
        title=idea.title,
        desc_md=idea.desc_md,
        desc_html=idea.desc_html,
        status=idea.status,
        vote_count=idea.vote_count,
        created_on=idea.created_on.strftime('%a, %d %b %Y %H:%M:%S'),
        # tags=idea.tags,
        # url=idea.url,
        # comments_url=idea.comments_url,
        # user=idea.user
    )
    return json
