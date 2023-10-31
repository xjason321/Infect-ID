import Player as p
import Graph as graph
import Algorithm as a
import os
import random
import math
import datetime

from flask import Flask, render_template, request, redirect, url_for
from Algorithm import run_ai


app = Flask(__name__, template_folder='templates', static_folder='static')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/home')
def home():
  return render_template('index.html')

@app.route('/howto')
def howto():
  return render_template('how-to.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/user-choice', methods=['GET', 'POST'])
def main():
  message = ""
  if request.args.get('failed') == "True":
    message = "Please upload a valid CSV."
  return render_template('transition.html', message=message)

@app.route('/process', methods=['POST'])
def process():
    # Retrieve the uploaded file
    uploaded_file = request.files['file']

    # Handle the uploaded file (e.g., save it to a folder)
    if uploaded_file:
      # Define the target directory to save the file
      target_directory = 'uploads'        
      uploaded_file.save(f'{target_directory}/{uploaded_file.filename}')

      filename = f'{target_directory}/{uploaded_file.filename}'

      file_name_with_extension = os.path.basename(filename)
      title = os.path.splitext(file_name_with_extension)[0]
      
      # Redirect to another route and pass parameters
      return redirect(url_for('visual', directory=filename, isUserUploaded="True", title=title))

@app.route('/visual', methods=['GET', 'POST'])
def visual():
  if request.args.get('isUserUploaded') == "True":
    try:
      csv_path = request.args.get('directory')

      player = p.Player(17, 2, 3, 4, 0.1, csv_pathway=csv_path)

      player.load_csv()

      os.remove(csv_path)

      title = request.args.get('title')
    except:
      try:
        os.remove(csv_path)
      except:
        pass
      return redirect(url_for('main', failed="True"))
  else:      
    # Random pathway -------
    player = p.Player(
        size=random.randint(50, 150),
        time=random.randint(3, 5),
        min=random.randint(2, 3),
        max=random.randint(3, 4),
        percent=random.uniform(0.15, 0.25),  # initially given
    )
    #----------
    title = "Random Network"

  # Get the current date
  current_date = datetime.date.today()

  # Format the date as "MM/DD/YY"
  formatted_date = current_date.strftime("%m/%d/%y")
  
  # NEAT GENOME SHIT: (THESE ARE GENERATED)
  negativeEffectBias = 70.16
  positiveBias = 58.123
  positiveEffectBias = 22.98
  similarityWeight = 119.5
  percentSamples = 0
  percentTraced = 0
  
  # FOR GEORGE: Uncomment this and change Algorithm.py to match dictionary
  ai = a.Algorithm(
       size=player.size,

       # NEAT
       negativeEffectBias=negativeEffectBias,
       positiveBias=positiveBias,
       positiveEffectBias=positiveEffectBias,
       similarityWeight=similarityWeight)

  sorted, traced = run_ai(ai, player, percentSamples, percentTraced)
  
  # Start window loop
  nodes, edges = graph.CreateGraphHTML(player, "templates/index.html")

  numPositive, numNegative, numUnknown = 0, 0, 0
  for node in player.nodes.values():
    if node.visibleToPlayer == False:
      numUnknown += 1
    elif node.state == 1: 
      numPositive += 1
    elif node.state == 0:
      numNegative += 1
  
  return render_template('app.html',
                         nodes=nodes,
                         edges=edges,
                         num_nodes=len(player.nodes),
                         num_positive=numPositive,
                         num_negative=numNegative,
                         num_unknown=numUnknown,
                         alloted_time=player.time,
                         min=player.min_connections,
                         max=player.max_connections,
                         title=title,
                         date=formatted_date,
                         num_visible=player.num_visible_to_player)
