from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.database import db
from app.models import History
from app.utils.cloud_storage import (
    upload_file_to_cloud_storage,
    delete_file_from_cloud_storage,
    preprocess_image,
    load_model_from_local,
    decode_prediction
)
from datetime import datetime
import json

history_blueprint = Blueprint("history", __name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_user_id_from_session():
    """Get user_id from the session."""
    user_id = session.get('user_id')
    if not user_id:
        raise ValueError("User  not logged in")
    return user_id

@history_blueprint.route("/", methods=["POST"])
def post_scan():
    """Endpoint for scanning an image and saving the result to the database."""
    try:
        user_id = get_user_id_from_session()  # Get user_id from session

        # Get the uploaded file
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Validate the file extension
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Only png, jpg, and jpeg are allowed."}), 400

        # Create a unique filename
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"

        # Upload the file to Cloud Storage
        public_url = upload_file_to_cloud_storage(file, filename)
        if public_url is None:
            return jsonify({"error": "Failed to upload the file to Cloud Storage."}), 500

        # Preprocess the image
        image_array = preprocess_image(file)
        if image_array is None:
            return jsonify({"error": "Failed to preprocess the image."}), 400

        # Load the models for predictions
        model_conditions, model_type = load_model_from_local()

        # Predict skin conditions and skin type
        predictions_skin_conditions = model_conditions.predict(image_array)
        predictions_skin_type = model_type.predict(image_array)

        # Decode the predictions
        skin_conditions_labels = ["Acne", "Eye Bags", "Normal"]
        skin_type_labels = ["Oily", "Normal", "Dry"]

        decoded_skin_conditions = decode_prediction(predictions_skin_conditions, skin_conditions_labels, threshold=0.5)
        decoded_skin_type = decode_prediction(predictions_skin_type, skin_type_labels, threshold=0.5)

        # Save the result to the database
        new_entry = History(
            user_id=user_id,
            filename=filename,
            predictions_skin_type=json.dumps(decoded_skin_type),
            predictions_skin_conditions=json.dumps(decoded_skin_conditions),
            timestamp=datetime.utcnow(),
        )
        db.session.add(new_entry)
        db.session.commit()

        # Return the result
        return jsonify({
            "user_id": user_id,
            "filename": filename,
            "skin_conditions": decoded_skin_conditions,
            "skin_type": decoded_skin_type,
            "image_url": public_url
        }), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401  # User not logged in
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_blueprint.route("/history", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
def get_history():
    """Endpoint for getting the user's scan history."""
    try:
        user_id = str(get_jwt_identity())  # Get user_id from JWT token

        # Get all history entries based on user_id
        history_entries = History.query.filter_by(user_id=user_id).order_by(History.timestamp.desc()).all()

        # Convert history data to JSON format
        history_data = [
            {
                "id": entry.id,
                "filename": entry.filename,
                "predictions_skin_type": json.loads(entry.predictions_skin_type),  # Convert JSON string back to dict
                "predictions_skin_conditions": json.loads(entry.predictions_skin_conditions),  # Convert JSON string back to dict
                "timestamp": entry.timestamp.isoformat(),
            }
            for entry in history_entries
        ]

        return jsonify({"history": history_data}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@history_blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()  # Ensure the user is authenticated
def delete_history(id):
    """Endpoint for deleting a scan history entry."""
    try:
        user_id = str(get_jwt_identity())  # Get user_id from JWT token

        # Find the history entry by ID and user_id
        history_entry = History.query.filter_by(id=id, user_id=user_id).first()
        if not history_entry:
            return jsonify({"error": "History not found"}), 404

        # Delete the file from Cloud Storage
        try:
            delete_file_from_cloud_storage(history_entry.filename)
        except Exception as e:
            return jsonify({"error": f"Failed to delete file from cloud storage: {str(e)}"}), 500

        # Delete the data from the history table
        db.session.delete(history_entry)
        db.session.commit()

        return jsonify({"message": "History entry deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500