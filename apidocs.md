Ideabin-

API endpoints

0. /ideabin/api/v1.0/
1. /ideabin/api/v1.0/ideas
2. /ideabin/api/v1.0/ideas/id
4. /ideabin/api/v1.0/ideas/tags
5. /ideabin/api/v1.0/ideas/tags/tagid
6. /ideabin/api/v1.0/users/
7. /ideabin/api/v1.0/users/userid

params-

        images
                id
                urls

        tags
                id
                title
                description (may be)
                ideas - list of ids associated

        idea
                id
                title (short description)
                description
                upvotes
                downvotes
                user (anonymous/userid)
                comments
                tags - list of tagids associated
                status - (someone's working, solved, open to all)
                images - list of images associated

        users
                id
                email(s)
                ideas submitted
                ideas upvoted
                ideas downvoted
                drafts
