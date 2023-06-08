
from flask import Flask, request, render_template


#Create an app object using the Flask class.
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

@app.route('/pell',methods=['POST','GET'])



def pell():
    lookup_table = {"48DC":
                        {2:  18310,
                         3:  23030,
                         4:  27750,
                         5:  32470,
                         6:  37190,
                         7:  41910,
                         8:  46630,
                         9:  4720 },

                    "AK":
                        {2:  22890,
                         3:  28790,
                         4:  34690,
                         5:  40590,
                         6:  46490,
                         7:  52390,
                         8:  58290,
                         9:  5900,
                         },
                    "HI":
                        {2:  21060,
                         3:  26490,
                         4:  31920,
                         5:  37350,
                         6:  42780,
                         7:  48210,
                         8:  53640,
                         9:  5430},

                    1: {"max": 2.25,"min": 3.25},

                    2: {"max": 1.75,"min": 2.75},
                }

    result = ""

    age = parents = siblings = live = -1

    if 'age' in request.form:
      try:
        age = int(request.form['age'])
      except:
        pass

    if 'parents' in request.form:
      try:
        parents = int(request.form['parents'])
      except:
        pass

    if 'siblings' in request.form:
      try:
        siblings = int(request.form['siblings'])
      except:
        pass

    if 'live' in request.form:
      try:
        live = request.form['live']
      except:
        pass

    missing = []
    if age == -1:
      missing.append("age.")
    if parents == -1:
      missing.append("parents.")
    if siblings == -1:
      missing.append("siblings.")
    if live == -1:
      missing.append("location.")
    if missing:
       return render_template('questions.html', result=["Please complete the form. You are missing:"] + missing)

    if age > 24:
      result = [f"Sorry, we don't handle non dependent adults." ]
      return render_template('results.html', result=result)

    if parents == 0:
      result = [f"Please select the number of parents you live with." ]
      return render_template('results.html', result=result)

    if live == "NOTUS":
      result = [f"Sorry, you have to be a US resident to be eligible for a Pell Grant."]
      return render_template('results.html', result=result)



    if live not in lookup_table:
      result = [f"sorry we dont have that data yet for live={live}"]
      return render_template('results.html', result=result)

    if parents not in lookup_table:
      result = [f"sorry we dont have that data yet for parents={parents}"]
      return render_template('results.html', result=result)

    deps = lookup_table[live]
    family_size = parents + siblings + 1 #the student
    if family_size > 8:
      pov_level = deps[8] + (family_size - 8) * deps[9]
    else:
      pov_level = deps[family_size]


    max_pell = pov_level * lookup_table[parents]["max"]
    min_pell = pov_level * lookup_table[parents]["min"]

    result = [f"You live with {parents} parent(s), with {siblings} sibling(s), in {live}:",
              f"If your family's Annual Gross Income (AGI) is less than ${max_pell:2.2f}, then you are entitled to the maximun Pell Grant ($5000 pa).",
              f"If your family's AGI is greater than ${min_pell:2.2f}, then unfortunately you are not eligble for any Pell Grant." ,
              f"If your family's AGI is between these two amounts, you are entitled to a proportion of the Pell Grant."]
    return render_template('results.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
