import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from typing import Dict, List, Any, Optional
import joblib
import os
from datetime import datetime, timedelta

class AIService:
    """
    AI Service for financial predictions and anomaly detection.

    This service provides methods for training and using machine learning models to
    predict spending, detect anomalies in transactions, and generate financial insights.
    """
    
    def __init__(self):
        """
        Initializes the AIService.
        """
        self.spending_model = None
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.model_path = "./models"
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
        
        # Load pre-trained models if they exist
        self._load_models()
    
    def _load_models(self):
        """
        Load pre-trained models from disk.
        """
        try:
            spending_model_path = os.path.join(self.model_path, "spending_predictor.joblib")
            if os.path.exists(spending_model_path):
                self.spending_model = joblib.load(spending_model_path)
                
            anomaly_model_path = os.path.join(self.model_path, "anomaly_detector.joblib")
            if os.path.exists(anomaly_model_path):
                self.anomaly_detector = joblib.load(anomaly_model_path)
                
            scaler_path = os.path.join(self.model_path, "scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                
        except Exception as e:
            print(f"Error loading models: {e}")
    
    def _save_models(self):
        """
        Save trained models to disk.
        """
        try:
            if self.spending_model:
                joblib.dump(self.spending_model, os.path.join(self.model_path, "spending_predictor.joblib"))
                
            if self.anomaly_detector:
                joblib.dump(self.anomaly_detector, os.path.join(self.model_path, "anomaly_detector.joblib"))
                
            joblib.dump(self.scaler, os.path.join(self.model_path, "scaler.joblib"))
            
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def prepare_features(self, transactions: List[Dict]) -> pd.DataFrame:
        """
        Prepare features from transaction data.

        Args:
            transactions (List[Dict]): A list of transaction dictionaries.

        Returns:
            pd.DataFrame: A DataFrame with the prepared features.
        """
        if not transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame(transactions)
        
        # Convert dates
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        
        # Extract time-based features
        df['day_of_week'] = df['transaction_date'].dt.dayofweek
        df['day_of_month'] = df['transaction_date'].dt.day
        df['month'] = df['transaction_date'].dt.month
        df['hour'] = df['transaction_date'].dt.hour
        
        # Create rolling statistics
        df = df.sort_values('transaction_date')
        df['rolling_mean_7d'] = df['amount'].rolling(window=7, min_periods=1).mean()
        df['rolling_std_7d'] = df['amount'].rolling(window=7, min_periods=1).std().fillna(0)
        
        # Category encoding (simple label encoding for now)
        categories = df['category'].fillna('unknown').unique()
        category_map = {cat: idx for idx, cat in enumerate(categories)}
        df['category_encoded'] = df['category'].fillna('unknown').map(category_map)
        
        return df
    
    def train_spending_predictor(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Train a model to predict future spending.

        Args:
            transactions (List[Dict]): A list of transaction dictionaries.

        Returns:
            Dict[str, Any]: A dictionary containing the training results.
        """
        df = self.prepare_features(transactions)
        
        if len(df) < 10:  # Need minimum data for training
            return {"success": False, "message": "Insufficient data for training"}
        
        # Prepare features and target
        feature_columns = [
            'day_of_week', 'day_of_month', 'month', 'hour',
            'category_encoded', 'rolling_mean_7d', 'rolling_std_7d'
        ]
        
        X = df[feature_columns].fillna(0)
        y = df['amount']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.spending_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        self.spending_model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.spending_model.score(X_train_scaled, y_train)
        test_score = self.spending_model.score(X_test_scaled, y_test)
        
        # Save model
        self._save_models()
        
        return {
            "success": True,
            "train_score": float(train_score),
            "test_score": float(test_score),
            "message": "Spending predictor trained successfully"
        }
    
    def predict_spending(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict spending amount based on features.

        Args:
            features (Dict[str, Any]): A dictionary of features for prediction.

        Returns:
            Dict[str, Any]: A dictionary containing the prediction results.
        """
        if not self.spending_model:
            return {"success": False, "message": "Model not trained"}
        
        try:
            # Prepare feature vector
            feature_vector = np.array([[
                features.get('day_of_week', 0),
                features.get('day_of_month', 1),
                features.get('month', 1),
                features.get('hour', 12),
                features.get('category_encoded', 0),
                features.get('rolling_mean_7d', 0),
                features.get('rolling_std_7d', 0)
            ]])
            
            # Scale features
            feature_vector_scaled = self.scaler.transform(feature_vector)
            
            # Make prediction
            prediction = self.spending_model.predict(feature_vector_scaled)[0]
            
            # Get prediction confidence (using variance of tree predictions)
            predictions = [tree.predict(feature_vector_scaled)[0] 
                         for tree in self.spending_model.estimators_]
            confidence = 1 / (1 + np.std(predictions))
            
            return {
                "success": True,
                "predicted_amount": float(prediction),
                "confidence": float(confidence),
                "message": "Prediction generated successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Prediction failed: {str(e)}"
            }
    
    def train_anomaly_detector(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Train anomaly detection model.

        Args:
            transactions (List[Dict]): A list of transaction dictionaries.

        Returns:
            Dict[str, Any]: A dictionary containing the training results.
        """
        df = self.prepare_features(transactions)
        
        if len(df) < 20:  # Need minimum data for anomaly detection
            return {"success": False, "message": "Insufficient data for anomaly detection training"}
        
        # Prepare features
        feature_columns = [
            'amount', 'day_of_week', 'day_of_month', 'month', 'hour',
            'category_encoded', 'rolling_mean_7d', 'rolling_std_7d'
        ]
        
        X = df[feature_columns].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train anomaly detector
        self.anomaly_detector = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42
        )
        
        self.anomaly_detector.fit(X_scaled)
        
        # Evaluate on training data
        anomaly_scores = self.anomaly_detector.decision_function(X_scaled)
        anomalies = self.anomaly_detector.predict(X_scaled)
        
        anomaly_count = np.sum(anomalies == -1)
        anomaly_percentage = (anomaly_count / len(anomalies)) * 100
        
        # Save model
        self._save_models()
        
        return {
            "success": True,
            "anomalies_detected": int(anomaly_count),
            "anomaly_percentage": float(anomaly_percentage),
            "message": "Anomaly detector trained successfully"
        }
    
    def detect_anomalies(self, transactions: List[Dict]) -> List[Dict[str, Any]]:
        """
        Detect anomalous transactions.

        Args:
            transactions (List[Dict]): A list of transaction dictionaries.

        Returns:
            List[Dict[str, Any]]: A list of anomalous transactions.
        """
        if not self.anomaly_detector:
            return []
        
        df = self.prepare_features(transactions)
        
        if df.empty:
            return []
        
        # Prepare features
        feature_columns = [
            'amount', 'day_of_week', 'day_of_month', 'month', 'hour',
            'category_encoded', 'rolling_mean_7d', 'rolling_std_7d'
        ]
        
        X = df[feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Detect anomalies
        anomaly_scores = self.anomaly_detector.decision_function(X_scaled)
        anomalies = self.anomaly_detector.predict(X_scaled)
        
        # Prepare results
        results = []
        for idx, (score, is_anomaly) in enumerate(zip(anomaly_scores, anomalies)):
            if is_anomaly == -1:  # Anomaly detected
                transaction = transactions[idx]
                results.append({
                    "transaction_id": transaction.get('id'),
                    "amount": transaction.get('amount'),
                    "description": transaction.get('description'),
                    "category": transaction.get('category'),
                    "transaction_date": transaction.get('transaction_date'),
                    "anomaly_score": float(score),
                    "severity": "high" if score < -0.5 else "medium"
                })
        
        return results
    
    def generate_insights(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Generate AI-powered financial insights.

        Args:
            transactions (List[Dict]): A list of transaction dictionaries.

        Returns:
            Dict[str, Any]: A dictionary of financial insights.
        """
        insights = {
            "spending_trends": [],
            "savings_opportunities": [],
            "budget_recommendations": [],
            "risk_alerts": []
        }
        
        if not transactions:
            return insights
        
        df = pd.DataFrame(transactions)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        
        # Spending trends
        monthly_spending = df.groupby(df['transaction_date'].dt.to_period('M'))['amount'].sum()
        if len(monthly_spending) >= 2:
            trend = "increasing" if monthly_spending.iloc[-1] > monthly_spending.iloc[-2] else "decreasing"
            change_pct = ((monthly_spending.iloc[-1] - monthly_spending.iloc[-2]) / monthly_spending.iloc[-2]) * 100
            
            insights["spending_trends"].append({
                "insight": f"Your spending is {trend} by {abs(change_pct):.1f}% compared to last month",
                "trend": trend,
                "change_percentage": float(change_pct)
            })
        
        # Category analysis for savings opportunities
        category_spending = df.groupby('category')['amount'].agg(['sum', 'count']).reset_index()
        category_spending['avg_transaction'] = category_spending['sum'] / category_spending['count']
        
        # Find categories with high spending
        high_spending_categories = category_spending.nlargest(3, 'sum')
        for _, cat in high_spending_categories.iterrows():
            insights["savings_opportunities"].append({
                "category": cat['category'],
                "total_spent": float(cat['sum']),
                "suggestion": f"Consider reviewing your {cat['category']} expenses - you've spent ${cat['sum']:.2f} in this category"
            })
        
        return insights