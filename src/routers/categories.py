from flask import Blueprint, request, jsonify, Response
from typing import Any

from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.models.category import Category
from src.core.db import db
from src.dtos.categories import CategoryCreateRequest, CategoryResponse, CategoryUpdateRequest

categories_bp = Blueprint("categories", __name__, url_prefix='/categories')

@categories_bp.route('/create', methods=["POST"])
def create_new_categories():
    try:
        raw_data: dict[str, Any] = request.get_json()

        if not raw_data:
            return jsonify(
                {
                    "error": "Validation Error",
                    "message": "No raw data found"
                }
            ), 400

        category_data = CategoryCreateRequest.model_validate(raw_data)

        category = Category(name=category_data.name)
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)



        return jsonify(
            CategoryResponse.model_validate(category).model_dump()
        ), 201

    except ValidationError as exc:
        return jsonify(
            {
                "error": "Validation Error",
                "message": exc.errors()
            }
        ), 400
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify(
            {
                "error": "DATABASE Error",
                "message": str(exc)
            }
        ), 400  # BAD REQUEST
    except Exception as exc:
        return jsonify(
            {
                "error": "Unexpected Error",
                "message": str(exc)
            }
        ), 500


@categories_bp.route('', methods=["GET"])
def list_of_categories() -> list[dict[str, Any]]:
    try:
        categories = Category.query.all()
        return jsonify(
            [
                CategoryResponse.model_validate(category).model_dump()
                for category in categories
            ]
        )
    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500

@categories_bp.route('/<int:category_id>', methods=["DELETE"])
def delete_categories(category_id: int) -> str:
    try:
        category = Category.query.get(category_id)

        if not category:
            return jsonify(
                {
                    "error": "Not Found",
                    "message": f"Category with ID {category_id} was not found"
                }
            ), 404

        if category.polls:
            for poll in category.polls:
                poll.category_id = None

        db.session.delete(category)
        db.session.commit()

        message = f"Category with ID {category_id} was deleted successfully."

        return jsonify({
                "message": message
            })
    except SQLAlchemyError as exc:
        db.session.rollback()
        return jsonify({
            "error": "DATABASE Error",
            "message": str(exc)
        }), 400
    except Exception as exc:
        return jsonify(
            {
                "error": "Unexpected Error",
                "message": str(exc)
            }
        ), 500

@categories_bp.route('/<int:categories_id>/update', methods=["PUT", "PATCH"])
def update_categories(categories_id: int) -> tuple[Response, int] | Response:
    try:
        raw_data: dict[str, Any] = request.get_json()
        if not raw_data:
            return jsonify(
                {
                    "error": "Validation Error",
                    "message": "No raw data found"
                }
            ), 400
        category = Category.query.get(categories_id)

        if not category:
            return jsonify(
                {
                    "error": "Not Found",
                    "message": f"Category with ID {categories_id} was not found"
                }
            ), 404
        updated_data = CategoryUpdateRequest.model_validate(raw_data)
        category.name = updated_data.name


        db.session.commit()
        db.session.refresh(category)
        return jsonify(
            CategoryResponse.model_validate(category).model_dump()
        )

    except ValidationError as exc:
        return jsonify({
            "error": "Validation Error",
            "message": exc.errors()
        }), 400
    except SQLAlchemyError as exc:
        return jsonify({
            "error": "DATABASE Error",
            "message": str(exc)
        }), 400
    except Exception as exc:
        return jsonify({
            "error": "Unexpected Error",
            "message": str(exc)
        }), 500
