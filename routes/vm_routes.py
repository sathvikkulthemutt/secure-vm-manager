from flask import Blueprint, request, jsonify
from core import vm_manager

vm_bp = Blueprint("vm_bp", __name__)


@vm_bp.route("/create", methods=["POST"])
def create_vm():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request"}), 400
    result = vm_manager.create_vm(
        name=data["name"], image=data.get("image", "ubuntu:22.04")
    )
    return jsonify(result)


@vm_bp.route("/start", methods=["POST"])
def start_vm():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request"}), 400
    result = vm_manager.start_vm(data["name"])
    return jsonify(result)


@vm_bp.route("/stop", methods=["POST"])
def stop_vm():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request"}), 400
    result = vm_manager.stop_vm(data["name"])
    return jsonify(result)


@vm_bp.route("/delete", methods=["POST"])
def delete_vm():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request"}), 400
    result = vm_manager.remove_vm(data["name"])
    return jsonify(result)


@vm_bp.route("/list", methods=["GET"])
def list_vms():
    result = vm_manager.list_vms()
    return jsonify(result)


@vm_bp.route("/snapshot", methods=["POST"])
def snapshot_vm():
    data = request.get_json()
    if not data or "name" not in data or "snapshot_name" not in data:
        return jsonify({"error": "Missing 'name' or 'snapshot_name' in request"}), 400
    result = vm_manager.snapshot_vm(data["name"], data["snapshot_name"])
    return jsonify(result)


@vm_bp.route("/restore", methods=["POST"])
def restore_vm():
    data = request.get_json()
    if not data or "snapshot_name" not in data or "new_vm_name" not in data:
        return jsonify({"error": "Missing 'snapshot_name' or 'new_vm_name' in request"}), 400
    result = vm_manager.restore_vm(data["snapshot_name"], data["new_vm_name"])
    return jsonify(result)
