from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note
import json

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) <1:
            flash('Note is too short',category='error')
            
        else:
            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!",category='success')
    return render_template('home.html',User=current_user)

from flask import jsonify, request

@views.route('/delete-note', methods=['POST','DELETE','GET'])
def delete_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    note = Note.query.get(note_id)

    if note:
        if note.user_id == current_user.id:
            try:
                db.session.delete(note)
                db.session.commit()
                return jsonify({ "message": "Note deleted successfully" })
            except Exception as e:
                return jsonify({"error": "Failed to delete the note", "details": str(e)}), 500
        else:
            return jsonify({"error": "You do not have permission to delete this note"}), 403
    else:
        return jsonify({"error": "Note not found"}), 404

@views.route('/delete/<int:note_id>', methods=['POST','DELETE','GET'])    
@login_required
def delete(note_id):
    note = Note.query.get_or_404(note_id)

    if note:
        if note.user_id == current_user.id:
            try:
                db.session.delete(note)
                db.session.commit()
                return redirect('/')
                #return jsonify({"message": "note deleted successfully"})
            except Exception as e:
                return jsonify({'error': 'Failed to delete the note', 'details': str(e)}), 500
        else:
            return jsonify({'error': 'You do not have permission to delete this note'}), 403
    else:
        return jsonify({'error': 'Note not found'}), 404
    
    
