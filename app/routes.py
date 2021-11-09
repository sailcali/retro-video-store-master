from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime


customer_bp = Blueprint('customer_bp',__name__, url_prefix='/customers')
video_bp = Blueprint('video_bp',__name__, url_prefix='/videos')

@video_bp.route('', methods=['GET', 'POST'])
def video_tasks():
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
        return jsonify(videos_response)

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

@video_bp.route('/<video_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_video_tasks(video_id):
    try:
        int(video_id)
    except ValueError:
        return make_response({'message': f'Video ID must be whole integer'}, 400)
    video = Video.query.get(video_id)
    if video is None:
        return make_response({'message': f'Video {video_id} was not found'}, 404)
    if request.method == 'GET':
        return {"id": video.id,
            "title": video.title,
            "total_inventory": video.total_inventory,
            "release_date": video.release_date
        }
    elif request.method == 'PUT':
        
        form_data = request.get_json()
        if 'title' not in form_data or 'release_date' not in form_data or 'total_inventory' not in form_data:
            return make_response('', 400)
        video.title = form_data["title"]
        video.release_date = form_data["release_date"]
        video.total_inventory = form_data["total_inventory"]

        db.session.commit()

        return make_response({"id": video.id,
                "title": video.title,
                "release_date": video.release_date,
                "total_inventory": video.total_inventory
            }, 200)
    elif request.method == 'DELETE':
        # name = video.title
        db.session.delete(video)
        db.session.commit()
        return make_response({
                             "id": video.id
                             }, 200)

def make_customer_dict(customer): 
    return {
        "id" : customer.id,
        "name" : customer.name,
        "postal_code" : customer.postal_code,
        "phone" : customer.phone,
        "registered_at" : customer.registered_at,
        } 

@customer_bp.route("", methods=["GET", "POST"])
def handle_customers():
    if request.method == "GET":       
        customers = Customer.query.all()

        customers_response = []
        for customer in customers:
            current_customer = make_customer_dict(customer)
            customers_response.append(current_customer)
            
        return jsonify(customers_response), 200
    # POST
    else: 
        request_body = request.get_json()
        # if post is missing postal code, name, or phone number do not post and return 400
        if "postal_code" not in request_body:
            return {"details": "Request body must include postal_code."}, 400
        elif "phone" not in request_body:
            return {"details": "Request body must include phone."}, 400
        elif "name" not in request_body:
            return {"details": "Request body must include name."}, 400
        # if all required values are given in the request body, return the task info with 201
        else: 
            new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"],
            registered_at=datetime.now()
        )
        db.session.add(new_customer)
        db.session.commit()

        return make_customer_dict(new_customer), 201

@customer_bp.route("/<id>", methods=["GET", "PUT", "DELETE"])
def handle_one_customer(id):
    try:
        int_id = int(id)
    except ValueError:
        return jsonify(""), 400

    customer = Customer.query.get(id)
    
    # Guard clause 
    if customer is None:
        return jsonify({"message": (f'Customer {id} was not found')}), 404
    
    
    if request.method == "GET": 
        return jsonify(make_customer_dict(customer)), 200
        
    elif request.method == "PUT":
        form_data = request.get_json()
        if "postal_code" not in form_data or "phone" not in form_data or "name" not in form_data:
            return jsonify(""), 400

        customer.name = form_data["name"]
        customer.postal_code = form_data["postal_code"]
        customer.phone = form_data["phone"]

        db.session.commit()
        return jsonify(make_customer_dict(customer)), 200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return jsonify({"id": customer.id}), 200