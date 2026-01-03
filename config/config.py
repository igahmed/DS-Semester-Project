import os

class Config:
    # Dashboard settings
    DASHBOARD_TITLE = "AI Cyber Threat Detection System"
    
    # File paths
    THREAT_HISTORY_FILE = 'logs/threats.json'
    LIVE_LOGS_FILE = 'logs/live_logs.json'
    
    # Threat level colors
    THREAT_COLORS = {
        'low': '#28a745',
        'medium': '#ffc107', 
        'high': '#dc3545'
    }
    
    # LLM Integration Point
    LLM_ENDPOINT = "http://localhost:8000/analyze"
    
    # ML Integration Point
    ML_MODEL_PATH = 'E:\DSA-Project\isolation_forest.pkl'
    
    # Simulation settings
    SIMULATION_ENABLED = True
    LOG_SIMULATION_RATE = 5  # logs per second
    
    # Theme settings
    THEMES = {
        'dark': {
            'primary_color': '#1E3A8A',
            'bg_color': '#0f172a',
            'text_color': '#f8fafc',
            'card_bg': '#1e293b',
            'border_color': '#334155'
        },
        'blue': {
            'primary_color': '#1E40AF',
            'bg_color': '#dbeafe',
            'text_color': '#1e3a8a',
            'card_bg': '#eff6ff',
            'border_color': '#93c5fd'
        },
        'light': {
            'primary_color': '#3B82F6',
            'bg_color': '#ffffff',
            'text_color': '#1f2937',
            'card_bg': '#f9fafb',
            'border_color': '#e5e7eb'
        }
    }