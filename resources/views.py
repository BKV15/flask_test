from flask import Blueprint, render_template , request , flash , redirect , url_for , jsonify
from flask_login import current_user , login_required
from .models import User , Note , Entities
import json
from .huggingfaceapi import query_ner , query_asr

views = Blueprint('views' , __name__)

@views.route('/')
def index():
    if current_user.is_authenticated:
        flash('You are already logged in' , category='error')
        return redirect(url_for('views.ner'))
    return render_template('index.html' , user=current_user)

@views.route('/ner' , methods=('GET' , 'POST'))
@login_required
def ner():

    if request.method == 'POST':
        
        data = request.form.get('note')
        outputs , state = query_ner(data)

        if state != 200:
            flash('Sorry servers are busy. Try again next time!' , category='error')
            return redirect(url_for('views.ner'))
        
        user = User.objects(id=current_user.id).first()
        note = Note(text=data)
        user.notes.append(note)

        for output in outputs:

            entity = output['entity_group']
            score = output['score']
            word = output['word']
            start_index = output['start']
            end_index = output['end']

            new_entity = Entities(entity=entity,score=score,word=word,start_index=start_index,end_index=end_index)
            note.entities.append(new_entity)
        
        user.save()
        return redirect(url_for('views.ner'))

    return render_template('ner.html' , user=current_user)

@views.route('/delete-note' , methods=('POST',))
@login_required
def delete_note():

    data = json.loads(request.data)
    note_id = data['noteId']
    user = User.objects(id=current_user.id).first()
    
    if note_id:
        user.update(pull__notes__id=note_id)
        user.save()

    return jsonify({})

@views.route('/asr' , methods=('GET' , 'POST'))
@login_required
def audio_processing():

    if request.method == 'POST':

        file = request.files['audio']
        data = file.read()

        output , state = query_asr(data)

        if state != 200:
            flash('Sorry servers are busy. Try again next time!' , category='error')
            return redirect(url_for('views.audio_processing'))
        
        
        return render_template('asr.html' , user=current_user , transcript=output['text'])

    return render_template('asr.html' , user=current_user , transcript=None)
