from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

# Route for a Home page
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predictdata', methods = ['GET','POST'])
def predict_datapoint():
    if request.method =='GET':
        return render_template('home.html')
    else:
        data = CustomData(
            age = int(request.form.get('age')),
            bmi = float(request.form.get('bmi')),
            avg_glucose_level = float(request.form.get('avg_glucose_level')),
            gender=request.form.get('gender'),
            ever_married=request.form.get('ever_married'),
            Residence_type=request.form.get('Residence_type'),
            work_type=request.form.get('work_type'),
            smoking_status=request.form.get('smoking_status'),
            hypertension=int(request.form.get('hypertension')),
            heart_disease=int(request.form.get('heart_disease'))
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline = PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)   