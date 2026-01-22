"""
ML Model Training Script for AI-NutriCare
Trains models for health condition classification with 90%+ accuracy target
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import joblib
from pathlib import Path
import json
import warnings
warnings.filterwarnings('ignore')

class HealthModelTrainer:
    """Train and evaluate health condition classification models"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.models = {}
        self.scaler = StandardScaler()
        self.model_dir = Path(__file__).parent.parent.parent / "models"
        self.model_dir.mkdir(exist_ok=True)
        
    def load_diabetes_data(self):
        """Load Pima Indians Diabetes dataset"""
        try:
            # Try to load from Kaggle download
            kaggle_path = Path(__file__).parent.parent.parent / "data" / "kaggle_datasets" / "pima-indians-diabetes-database" / "diabetes.csv"
            if kaggle_path.exists():
                df = pd.read_csv(kaggle_path)
                print(f"✅ Loaded data from Kaggle: {len(df)} records")
            else:
                # Generate synthetic data if Kaggle data not available
                print("⚠️  Kaggle data not found. Generating synthetic dataset...")
                df = self._generate_synthetic_diabetes_data()
                print(f"✅ Generated synthetic data: {len(df)} records")
            
            return df
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            print("Generating synthetic dataset...")
            return self._generate_synthetic_diabetes_data()
    
    def _generate_synthetic_diabetes_data(self, n_samples=1000):
        """Generate synthetic diabetes dataset for training"""
        np.random.seed(42)
        
        # Generate realistic medical data
        data = {
            'Pregnancies': np.random.randint(0, 15, n_samples),
            'Glucose': np.random.normal(120, 30, n_samples).clip(70, 200),
            'BloodPressure': np.random.normal(70, 12, n_samples).clip(50, 120),
            'SkinThickness': np.random.normal(20, 15, n_samples).clip(0, 99),
            'Insulin': np.random.normal(80, 115, n_samples).clip(0, 846),
            'BMI': np.random.normal(32, 7, n_samples).clip(18, 60),
            'DiabetesPedigreeFunction': np.random.uniform(0.08, 2.42, n_samples),
            'Age': np.random.randint(21, 81, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate outcome based on realistic rules
        df['Outcome'] = 0
        df.loc[(df['Glucose'] > 140) | (df['BMI'] > 35), 'Outcome'] = 1
        df.loc[(df['Glucose'] > 126) & (df['Age'] > 45), 'Outcome'] = 1
        df.loc[(df['Glucose'] > 100) & (df['BMI'] > 30) & (df['Age'] > 40), 'Outcome'] = 1
        
        # Add some randomness
        flip_indices = np.random.choice(df.index, size=int(0.15 * len(df)), replace=False)
        df.loc[flip_indices, 'Outcome'] = 1 - df.loc[flip_indices, 'Outcome']
        
        return df
    
    def prepare_data(self, df):
        """Prepare data for training"""
        # Handle missing values (replace 0s with median for certain columns)
        zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
        for col in zero_cols:
            if col in df.columns:
                df[col] = df[col].replace(0, df[col].median())
        
        # Separate features and target
        X = df.drop('Outcome', axis=1)
        y = df['Outcome']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, X.columns.tolist()
    
    def train_random_forest(self, X_train, y_train):
        """Train Random Forest classifier with hyperparameter tuning"""
        print("\n🌲 Training Random Forest...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf = RandomForestClassifier(random_state=42)
        grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0)
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Best params: {grid_search.best_params_}")
        print(f"✅ Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def train_xgboost(self, X_train, y_train):
        """Train XGBoost classifier"""
        print("\n🚀 Training XGBoost...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'subsample': [0.8, 1.0]
        }
        
        xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
        grid_search = GridSearchCV(xgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0)
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Best params: {grid_search.best_params_}")
        print(f"✅ Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def train_lightgbm(self, X_train, y_train):
        """Train LightGBM classifier"""
        print("\n💡 Training LightGBM...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1, 0.3],
            'num_leaves': [31, 50, 70]
        }
        
        lgb_model = lgb.LGBMClassifier(random_state=42, verbose=-1)
        grid_search = GridSearchCV(lgb_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0)
        grid_search.fit(X_train, y_train)
        
        print(f"✅ Best params: {grid_search.best_params_}")
        print(f"✅ Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def create_ensemble(self, rf_model, xgb_model, lgb_model):
        """Create ensemble model combining all classifiers"""
        print("\n🎯 Creating Ensemble Model...")
        
        ensemble = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('xgb', xgb_model),
                ('lgb', lgb_model)
            ],
            voting='soft'
        )
        
        return ensemble
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """Evaluate model performance"""
        y_pred = model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"\n{'='*60}")
        print(f"📊 {model_name} Performance")
        print(f"{'='*60}")
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        print(f"{'='*60}")
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def save_models(self, models, feature_names):
        """Save trained models and metadata"""
        print("\n💾 Saving models...")
        
        # Save individual models
        for name, model in models.items():
            model_path = self.model_dir / f"{name}_model.pkl"
            joblib.dump(model, model_path)
            print(f"✅ Saved {name} to {model_path}")
        
        # Save scaler
        scaler_path = self.model_dir / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        print(f"✅ Saved scaler to {scaler_path}")
        
        # Save metadata
        metadata = {
            'feature_names': feature_names,
            'model_names': list(models.keys()),
            'training_date': pd.Timestamp.now().isoformat()
        }
        metadata_path = self.model_dir / "model_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Saved metadata to {metadata_path}")
    
    def train_all_models(self):
        """Complete training pipeline"""
        print("="*60)
        print("🏥 AI-NutriCare ML Model Training")
        print("="*60)
        
        # Load data
        df = self.load_diabetes_data()
        
        # Prepare data
        X_train, X_test, y_train, y_test, feature_names = self.prepare_data(df)
        
        print(f"\n📊 Dataset Info:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        print(f"   Features: {len(feature_names)}")
        
        # Train individual models
        rf_model = self.train_random_forest(X_train, y_train)
        xgb_model = self.train_xgboost(X_train, y_train)
        lgb_model = self.train_lightgbm(X_train, y_train)
        
        # Create ensemble
        ensemble_model = self.create_ensemble(rf_model, xgb_model, lgb_model)
        ensemble_model.fit(X_train, y_train)
        
        # Evaluate all models
        results = {}
        results['random_forest'] = self.evaluate_model(rf_model, X_test, y_test, "Random Forest")
        results['xgboost'] = self.evaluate_model(xgb_model, X_test, y_test, "XGBoost")
        results['lightgbm'] = self.evaluate_model(lgb_model, X_test, y_test, "LightGBM")
        results['ensemble'] = self.evaluate_model(ensemble_model, X_test, y_test, "Ensemble")
        
        # Save models
        models = {
            'random_forest': rf_model,
            'xgboost': xgb_model,
            'lightgbm': lgb_model,
            'ensemble': ensemble_model
        }
        self.save_models(models, feature_names)
        
        # Save results
        results_path = self.model_dir / "training_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "="*60)
        print("✅ Training Complete!")
        print("="*60)
        
        # Check if we achieved 90%+ accuracy
        best_accuracy = max(r['accuracy'] for r in results.values())
        if best_accuracy >= 0.90:
            print(f"🎉 SUCCESS! Achieved {best_accuracy*100:.2f}% accuracy (Target: 90%)")
        else:
            print(f"⚠️  Best accuracy: {best_accuracy*100:.2f}% (Target: 90%)")
            print("   Consider: More data, feature engineering, or hyperparameter tuning")
        
        return results

if __name__ == "__main__":
    trainer = HealthModelTrainer()
    results = trainer.train_all_models()
