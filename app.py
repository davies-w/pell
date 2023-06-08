
from flask import Flask, request, render_template


#Create an app object using the Flask class.
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/i_questions')
def i_questions():
    return render_template('i_questions.html')

@app.route('/d_questions')
def d_questions():
    return render_template('d_questions.html')


@app.route('/i_pell', methods=['POST','GET'])
def i_pell():
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


                    "1_48DC":
                        {1:  13590,
                         2:  18310,
                         3:  23030,
                         4:  27750,
                         5:  32470,
                         6:  37190,
                         7:  41910,
                         8:  46630,
                         9:  4720},

                    "1_AK":
                        {1:  16990,
                         2:  22890,
                         3:  28790,
                         4:  34690,
                         5:  40590,
                         6:  46490,
                         7:  52390,
                         8:  58290,
                         9:  5900,
                         },
                    "1_HI":
                        {1:  15630,
                         2:  21060,
                         3:  26490,
                         4:  31920,
                         5:  37350,
                         6:  42780,
                         7:  48210,
                         8:  53640,
                         9:  5430 },

                    1: {"max": 1.75,"min": 2.25}, #not parent

                    2: {"max": 2.25,"min": 4.0}, #single

                    3: {"max": 1.75,"min": 3.5}, #couple
                }

    result = ""

    parents = children = live = -1
    if 'parents' in request.form:
      try:
        parents = int(request.form['parents'])
      except:
        pass

    if 'children' in request.form:
      try:
        children = int(request.form['children'])
      except:
        pass

    if 'live' in request.form:
      try:
        live = request.form['live']
      except:
        pass

    missing = []

    if parents == -1:
      missing.append("parents.")
    if children == -1:
      missing.append("children.")
    if live == -1:
      missing.append("location.")
    if missing:
       return render_template('i_questions.html', result=["Please complete the form. You are missing:"] + missing)


    if live == "NOTUS":
      result = [f"Sorry, you have to be a US resident to be eligible for a Pell Grant."]
      return render_template('results.html', result=result)

    if parents == 1 and children > 0:
      return render_template('i_questions.html', result=["Try again, you can't be not a parent and have more than 0 children!"])

    if parents == 1:
       deps = lookup_table[f"1_{live}"]
    else:
       deps = lookup_table[live]
    family_size = parents -1  + children + 1 #the student
    if family_size > 8:
      pov_level = deps[8] + (family_size - 8) * deps[9]
    else:
      pov_level = deps[family_size]

    max_pell = pov_level * lookup_table[parents]["max"]
    min_pell = pov_level * lookup_table[parents]["min"]

    parental_status = {1: "not-a-parent", 2: "single-parent", 3: "couple"}[parents]

    result = [f"You are an independent student, {parental_status}, with {children} children, in {live}:",
              f"If your family's Annual Gross Income (AGI) is less than ${max_pell:2.2f}, then you are entitled to the maximun Pell Grant ($5000 pa).",
              f"If your family's AGI is greater than ${min_pell:2.2f}, then unfortunately you are not eligble for any Pell Grant." ,
              f"If your family's AGI is between these two amounts, you are entitled to a proportion of the Pell Grant."]
    return render_template('results.html', result=result)



@app.route('/d_pell',methods=['POST','GET'])
def d_pell():
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
    if age > 24:
      result = [f"You are over 24 years of age. Please fill out the indendepent version!"]
      return render_template('i_questions.html', result=result)

    if parents == -1:
      missing.append("parents.")
    if siblings == -1:
      missing.append("siblings.")
    if live == -1:
      missing.append("location.")
    if missing:
       return render_template('d_questions.html', result=["Please complete the form. You are missing:"] + missing)



    if live == "NOTUS":
      result = [f"Sorry, you have to be a US resident to be eligible for a Pell Grant."]
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
