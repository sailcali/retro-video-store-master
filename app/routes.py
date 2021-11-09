from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.video import Video
from app.models.customer import Customer


customer_bp = Blueprint('customer_bp',__name__, url_prefix='/customers')
video_bp = Blueprint('video_bp',__name__, url_prefix='/videos')

@customer_bp.route('', methods=['GET'])
def customer_info():
    pass

@video_bp.route('', methods=['GET', 'POST'])
def video_info():
    if request.method == 'GET':
        videos = Video.query.all()
        videos_response = []
        for video in videos:
            videos_response.append({
                    "id": video.id,
                    "title": video.title,
                    "release_date": video.release_date,
                    "total_inventory": video.total_inventory
                })
            # sort_query = request.args.get("sort")
            # if sort_query == 'asc':
            #     # tasks_response = sorted(tasks_response, key = lambda i: i['title'])
            # elif sort_query == 'desc':
            #     # tasks_response = sorted(tasks_response, key = lambda i: i['title'], reverse=True)
        return jsonify(videos_response), 200

    elif request.method == 'POST':
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response({'details': "Request body must include title."}, 400)
        elif 'release_date' not in request_body:
            return make_response({'details': "Request body must include release_date."}, 400)
        elif 'total_inventory' not in request_body:
            return make_response({'details': "Request body must include total_inventory."}, 400)
        else:
            new_video = Video(title=request_body["title"],
                            release_date=request_body["release_date"],
                            total_inventory=request_body["total_inventory"])

            db.session.add(new_video)
            db.session.commit()

            j = {'id': new_video.id,
                        'title': new_video.title,
                        'release_date': new_video.release_date,
                        'total_inventory': new_video.total_inventory}

            return make_response(j, 201)

