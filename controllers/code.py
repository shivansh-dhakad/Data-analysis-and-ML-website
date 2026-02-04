from flask import Blueprint, render_template, request, redirect, url_for, session,  send_file,jsonify
from flask_cors import CORS
import io
import base64
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

code = Blueprint("code", __name__)
df=None
@code.route("/", methods=["GET"])
def index():
    return redirect(url_for("code.login"))

@code.route("/login", methods=["GET", "POST"]) 
def login():
    return render_template("index.html")

@code.route("/upload", methods=["POST"])
def get_file():
    global df
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file received"}), 400

    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Invalid file type"}), 400

        print(df.head())
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

  
@code.route("/basic_info",methods=["GET", "POST"])
def basic_info():
    return render_template("basic_info.html")

@code.route("/visualization",methods=["GET", "POST"])
def visualization():
    return render_template("visualization.html")

@code.route("/processing",methods=["GET", "POST"])
def processing():
    return render_template("processing.html")

@code.route("/model",methods=["GET", "POST"])
def model():
    return render_template("model.html")
    
# =========================
# DATA PREVIEW ROUTES (robust for large data)
# =========================
@code.route("/head")
def head_data():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400
    try:
        data = df.head(5).replace({np.nan: None})
        return jsonify(data.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/tail")
def tail_data():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400
    try:
        data = df.tail(5).replace({np.nan: None})
        return jsonify(data.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/sample")
def sample_data():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400
    try:
        n = min(5, len(df))
        data = df.sample(n).replace({np.nan: None})
        return jsonify(data.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500



from io import StringIO

@code.route("/info")
def info():
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        buffer.close()
        return jsonify({"data": info_str})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@code.route("/describe")
def describe_data():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400
    try:
        # Describe works for all numeric columns automatically
        describe_df = df.describe()

        # Reset index so stats become a column
        describe_df = describe_df.reset_index().rename(columns={"index": "stat"})

        # Convert to records for JSON
        return jsonify(describe_df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/columns")
def columns():
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(exclude="number").columns.tolist()
        return jsonify({
            "numerical": num_cols,
            "categorical": cat_cols
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@code.route("/unique_values")
def unique_values():
    global df
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400

    col = request.args.get("column")

    if not col:
        return jsonify({"error": "No column selected"}), 400

    if col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    try:
        unique_vals = df[col].dropna().unique().tolist()

        # Convert numpy types to normal Python types
        clean_vals = [str(v) for v in unique_vals]

        return jsonify({"unique": clean_vals})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/missing")
def missing():
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        # Convert NaN to None so JSON can handle it
        missing_dict = df.isnull().sum().to_dict()
        clean_missing_dict = {k: (None if pd.isna(v) else v) for k, v in missing_dict.items()}
        return jsonify({"missing_values": clean_missing_dict})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@code.route("/shape")
def shape():
    global df
    if df is None:
        return jsonify({"error": "No data loaded"})
    return jsonify({"rows": df.shape[0], "columns": df.shape[1]})

    
@code.route("/duplicate")
def duplicate():
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        dup_count = int(df.duplicated().sum())
        return jsonify({"duplicated": dup_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/correlation")
def correlation():
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400
    try:
        # Only numeric columns
        numeric_df = df.select_dtypes(include='number')

        # correlation matrix
        corr_df = numeric_df.corr()

        # Convert all values to native float
        corr_dict = {col: {row: float(corr_df.loc[row, col]) 
                           for row in corr_df.index} 
                     for col in corr_df.columns}

        return jsonify({"correlation": corr_dict})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@code.route("/categorical")
def categorical():
    global df
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    return jsonify(cat_cols)


@code.route("/numerical")
def numerical():
    global df
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    
    num_cols = df.select_dtypes(include='number').columns.tolist()
    return jsonify(num_cols)

    
@code.route("/get_columns")
def get_columns():
    global df
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    return jsonify(list(df.columns))


@code.route("/countplot", methods=["POST"])
def countplot():
    global df
    col = request.json.get("column")

    if df is None:
        return jsonify({"error": "No data"}), 400

    if col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.countplot(x=df[col])
    plt.xticks(rotation=45)
    plt.title(f"Count Plot of {col}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img_base64})


@code.route("/piechart", methods=["POST"])
def piechart():
    global df
    col = request.json.get("column")

    if df is None:
        return jsonify({"error": "No data"}), 400

    if col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    df[col].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title(f"Pie Chart of {col}")
    plt.ylabel("")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img_base64})

@code.route("/histogram", methods=["POST"])
def histogram():
    global df
    col = request.json.get("column")

    if df is None or col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.histplot(df[col], kde=False)
    plt.title(f"Histogram of {col}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/kdeplot", methods=["POST"])
def kdeplot():
    global df
    col = request.json.get("column")

    if df is None or col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.kdeplot(df[col], fill=True)
    plt.title(f"KDE Plot of {col}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/boxplot", methods=["POST"])
def boxplot():
    global df
    col = request.json.get("column")

    if df is None or col not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.boxplot(y=df[col])
    plt.title(f"Boxplot of {col}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/scatterplot", methods=["POST"])
def scatterplot():
    colx = request.json.get("x")
    coly = request.json.get("y")

    if df is None or colx not in df.columns or coly not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.scatterplot(x=df[colx], y=df[coly])
    plt.title(f"{colx} vs {coly}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/boxplot_bi", methods=["POST"])
def boxplot_bi():
    x = request.json.get("x")
    y = request.json.get("y")
    hue = request.json.get("hue")

    if df is None or x not in df.columns or y not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.boxplot(x=df[x], y=df[y], hue=df[hue] if hue else None)
    plt.title(f"{x} vs {y}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})


@code.route("/distplot_bi", methods=["POST"])
def distplot_bi():
    x = request.json.get("x")
    y = request.json.get("y")

    if df is None or x not in df.columns or y not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.kdeplot(df[x], label=x)
    sns.kdeplot(df[y], label=y)
    plt.legend()
    plt.title(f"{x} vs {y}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/barplot_bi", methods=["POST"])
def barplot_bi():
    x = request.json.get("x")
    y = request.json.get("y")

    if df is None or x not in df.columns or y not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.barplot(x=df[x], y=df[y])
    plt.xticks(rotation=45)
    plt.title(f"{x} vs {y}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/lineplot_bi", methods=["POST"])
def lineplot_bi():
    x = request.json.get("x")
    y = request.json.get("y")

    if df is None or x not in df.columns or y not in df.columns:
        return jsonify({"error": "Invalid column"}), 400

    plt.clf()
    sns.lineplot(x=df[x], y=df[y])
    plt.title(f"{x} vs {y}")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img})

@code.route("/heatmap", methods=["GET"])
def heatmap():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400

    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        return jsonify({"error": "No numeric columns for heatmap"}), 400

    plt.clf()
    plt.figure(figsize=(8,6))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Correlation Heatmap")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()

    return jsonify({"image": img_base64})

@code.route("/pairplot", methods=["POST"])
def pairplot():
    global df
    if df is None:
        return jsonify({"error": "No data uploaded"}), 400

    kind = request.json.get("kind", "scatter")
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        return jsonify({"error": "No numeric columns for pair plot"}), 400

    plt.clf()
    sns.pairplot(numeric_df, kind=kind)
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    
    return jsonify({"image": img_base64})

@code.route("/columns_info")
def columns_info():
    global df
    try:
        numerical = df.select_dtypes(include=["int64","float64"]).columns.tolist()
        categorical = df.select_dtypes(include=["object","category"]).columns.tolist()
        return jsonify({"numerical": numerical, "categorical": categorical})
    except Exception as e:
        return jsonify({"error": str(e)})

# Handle missing
@code.route("/process/missing", methods=["POST"])
def process_missing():
    global df
    try:
        data = request.json
        col = data.get("column")
        method = data.get("method")

        if method == "drop":
            df = df.dropna(subset=[col])
        elif method == "mean":
            df[col] = df[col].fillna(df[col].mean())
        elif method == "median":
            df[col] = df[col].fillna(df[col].median())
        elif method == "mode":
            df[col] = df[col].fillna(df[col].mode()[0])

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


# Handle duplicates
# Handle duplicates with alert
@code.route("/process/duplicates", methods=["POST"])
def process_duplicates():
    global df
    try:
        method = request.json.get("method")

        if method == "drop":
            df = df.drop_duplicates()
            msg = "All duplicate rows removed."
        elif method == "keep_first":
            df = df.drop_duplicates(keep="first")
            msg = "Duplicates removed, first occurrence kept."
        elif method == "keep_last":
            df = df.drop_duplicates(keep="last")
            msg = "Duplicates removed, last occurrence kept."
        else:
            msg = "No action taken."

        return jsonify({"success": True, "message": msg})
    except Exception as e:
        return jsonify({"error": str(e)})



@code.route("/process/outlier", methods=["POST"])
def process_outlier():
    global df
    try:
        data = request.json
        col = data.get("column")
        q_low = float(data.get("q_low"))
        q_high = float(data.get("q_high"))

        low_val = df[col].quantile(q_low)
        high_val = df[col].quantile(q_high)

        df = df[(df[col] >= low_val) & (df[col] <= high_val)]

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})


# Change data type
@code.route("/process/dtype", methods=["POST"])
def process_dtype():
    global df
    try:
        data = request.json
        col = data.get("column")
        dtype = data.get("dtype")
        df[col] = df[col].astype(dtype)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

# Drop column
@code.route("/process/drop", methods=["POST"])
def process_drop():
    global df
    try:
        col = request.json.get("column")
        df = df.drop(columns=[col])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

# Download CSV
@code.route("/download")
def download_file():
    global df
    try:
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(
            io.BytesIO(buffer.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="processed_data.csv"
        )
    except Exception as e:
        return str(e)
    
    
    
# ----------------------------------------------------------------------------------------
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import numpy as np
X = None
y = None
X_train=None
X_test=None
y_train=None
y_test=None
y_pred=None
selected_numerical_cols = []
selected_categorical_cols = []
model=None

@code.route("/split_xy", methods=["POST"])
def split_xy():
    global df, X, y

    data = request.json
    target = data.get("target")

    if df is None:
        return jsonify({"error": "No dataset uploaded"}), 400

    if target not in df.columns:
        return jsonify({"error": "Invalid target column"}), 400

    y = df[target]
    X = df.drop(columns=[target])

    return jsonify({
        "message": "X and y created",
        "x_columns": X.columns.tolist(),
        "y_column": target
    })


@code.route("/train_test_split", methods=["POST"])
def train_test_split_route():
    global df, X, y, X_train, X_test, y_train, y_test

    if df is None:
        return jsonify({"error": "No dataset uploaded"}), 400

    data = request.json

    test_size = float(data.get("test_size"))
    random_state = int(data.get("random_state"))
    shuffle = data.get("shuffle") == "True"

    if X is None or y is None:
        return jsonify({"error": "Please split X and y first"}), 400

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        shuffle=shuffle
    )

    return jsonify({
        "message": "success",
        "test_size": test_size,
        "random_state": random_state,
        "shuffle": shuffle,
        "train_shape": X_train.shape,
        "test_shape": X_test.shape
    })
    
@code.route('/get_X_train_columns')
def Xtrain_cols():
    if df is None:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        num_cols = X_train.select_dtypes(include="number").columns.tolist()
        cat_cols = X_train.select_dtypes(exclude="number").columns.tolist()
        return jsonify({
            "numerical": num_cols,
            "categorical": cat_cols
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def pipeline(s,e,m):
    global model
    if s=='standardscaler':
        from sklearn.preprocessing import StandardScaler
        scaler=StandardScaler()
    elif s=='MinMaxscaler':
        from sklearn.preprocessing import MinMaxScaler
        scaler=MinMaxScaler()
    else:
        scaler=None
    if e=='Label' :
        from sklearn.preprocessing import LabelEncoder
        encoder=LabelEncoder()   
    elif e=='OnehotEncoder':
        from sklearn.preprocessing import OneHotEncoder
        encoder=OneHotEncoder(drop="first")
    else:
        encoder=None
    if m=='linear':
        from sklearn.linear_model import LinearRegression
        model_select=LinearRegression()
    elif m=='logistic':
        from sklearn.linear_model import LogisticRegression    
        model_select=LogisticRegression()
    elif m=='knnc':
        from sklearn.neighbors import KNeighborsClassifier
        model_select=KNeighborsClassifier()
    elif m=='knnr':
        from sklearn.neighbors import KNeighborsRegressor
        model_select=KNeighborsRegressor()
    elif m=='naive':
        from sklearn.naive_bayes import GaussianNB
        model_select=GaussianNB()
    elif m=='svc':
        from sklearn.svm import SVC
        model_select=SVC()
    elif m=='svr':
        from sklearn.svm import SVR
        model_select=SVR()
    elif m=='decisionc':
        from sklearn.tree import DecisionTreeClassifier
        model_select=DecisionTreeClassifier()
    elif m=='decisionr':
        from sklearn.tree import DecisionTreeRegressor
        model_select=DecisionTreeRegressor()
    elif m=='random_forestc':
        from sklearn.ensemble import RandomForestClassifier
        model_select=RandomForestClassifier()
    elif m=='random_forestr':
        from sklearn.ensemble import RandomForestRegressor
        model_select=RandomForestRegressor()
    print(scaler,encoder,model_select)
    transformers = []
    if selected_numerical_cols and scaler:
        transformers.append(('scaler', scaler, selected_numerical_cols))
    if selected_categorical_cols and encoder:
        transformers.append(('encoder', encoder, selected_categorical_cols))

    preprocessor = ColumnTransformer(transformers, remainder='passthrough')

    
    model= Pipeline([
        ('preprocessing',preprocessor),
        ('model_selection',model_select)
    ])
    print(model)
    
    

@code.route("/set_model_columns", methods=["POST"])
def set_model_columns():
    global selected_numerical_cols, selected_categorical_cols

    data = request.json
    selected_numerical_cols = data.get("numerical", [])
    selected_categorical_cols = data.get("categorical", [])
    scaler=data.get('scaling')
    encoder=data.get('encoding')
    model=data.get('model')
    if not selected_numerical_cols and not selected_categorical_cols:
        return jsonify({"error": "No columns selected"}), 400
    if  not model:
        return jsonify({"error":"select model first"})
    
    pipeline(scaler,encoder,model)
        
    return jsonify({
        "message": "Columns stored successfully",
        "numerical": selected_numerical_cols,
        "categorical": selected_categorical_cols,
        "scaler":scaler,
        "encoder":encoder,
        "model":model
    })

@code.route("/model_create", methods=["POST"])
def model_create():
    global model, X_train, X_test, y_train, y_test

    if model is None:
        return jsonify({"error": "Pipeline not created. Please create pipeline first."}), 400

    if X_train is None or y_train is None:
        return jsonify({"error": "Train-test split not done yet."}), 400

    try:
        model.fit(X_train, y_train)
        return jsonify({"message": "Model trained successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import numpy as np

@code.route("/model_evaluation")
def model_evaluation():
    global model, X_test, y_test,y_pred

    if model is None or X_test is None or y_test is None:
        return jsonify({"error": "Model not trained or test data not available"}), 400

    try:
        y_pred = model.predict(X_test)

        model_step = model.named_steps['model_selection']
        is_classifier = hasattr(model_step, "predict_proba") or hasattr(model_step, "classes_")

        plt.clf()

        # ===== CLASSIFICATION =====
        if is_classifier:
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            conf_matrix = confusion_matrix(y_test, y_pred).tolist()
            class_report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

            # Plot actual vs predicted
            plt.figure(figsize=(5,4))
            plt.scatter(range(len(y_test)), y_test, label="Actual")
            plt.scatter(range(len(y_pred)), y_pred, label="Predicted")
            plt.legend()
            plt.title("Actual vs Predicted (Classification)")

        # ===== REGRESSION =====
        else:
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            pred_df = pd.DataFrame({
                "Actual": y_test.values,
                "Predicted": y_pred
            }).head(10)

            predictions_table = pred_df.to_html(classes="eval-grid", index=False, border=0)


            plt.figure(figsize=(5,4))
            plt.scatter(y_test, y_pred, color="blue", label="Data points")

            # Fit a line (best fit)
            m, b = np.polyfit(y_test, y_pred, 1)  # slope and intercept
            plt.plot(y_test, m*y_test + b, linestyle="--", color="red", label="Best fit line")

            plt.xlabel("Actual")
            plt.ylabel("Predicted")
            plt.title("Best Fit Line")
            plt.legend()
            plt.show()


        # Convert plot to base64
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        plot_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close()

        if is_classifier:
            return jsonify({
                "model_type": "classification",
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "confusion_matrix": conf_matrix,
                "classification_report": class_report,
                "plot": plot_base64
            })
        else:
            return jsonify({
                "model_type": "regression",
                "r2_score": r2,
                "mse": mse,
                "rmse": rmse,
                "mae": mae,
                "target": y_test.name,
                "samples": len(y_test),
                "predictions_table": predictions_table,
                "plot": plot_base64
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@code.route("/export")
def export_file():
    global model
    try:
        import pickle
        if model is None:
            return jsonify({"error": "No trained model found"}), 400
        buffer = io.BytesIO()
        pickle.dump(model, buffer)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/octet-stream",
            as_attachment=True,
            download_name="model.pkl"
        )

    except Exception as e:
        return jsonify({"error": str(e)})
