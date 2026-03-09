import psycopg2
import os

# Connection parameters - support both Docker and local
DB_NAME = os.getenv('DB_NAME', 'intel')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'Password1!')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

schema_sql = """
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS notes CASCADE;
DROP TABLE IF EXISTS challenge_status CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    body TEXT NOT NULL,
    month VARCHAR(20) NOT NULL,
    scope VARCHAR(20) NOT NULL
);

CREATE TABLE challenge_status (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN DEFAULT FALSE
);

INSERT INTO users (username, password) VALUES
('analyst', 'Falcon2025!'),
('intel_ops', 'Raptor123');

-- Initialize challenge status as not completed
INSERT INTO challenge_status (id, completed) VALUES (1, FALSE);

-- CURRENT INTELLIGENCE (October 2025)
INSERT INTO notes (title, body, month, scope) VALUES
('ISR Mission Report - PACOM AOR', 'RQ-4 Global Hawk conducted reconnaissance over South China Sea. Detected 8 Type 052D destroyers conducting exercises 180nm east of Hainan Island. Electronic signatures consistent with SAM radar systems active.', '2025-10', 'current'),

('F-22 Deployment Status', 'Current Raptor deployment to Kadena AB, Okinawa includes 18 aircraft from 3rd Wing. Aircraft maintaining 95% mission capable rate. Next rotation scheduled for mid-November.', '2025-10', 'current'),

('Threat Assessment - Eastern Europe', 'Satellite imagery confirms increased activity at Kaliningrad AB. 12 Su-35S fighters observed along with S-400 battery deployment. Activity level elevated 40% compared to previous month.', '2025-10', 'current'),

('B-2 Exercise THUNDER BOLT', 'Two B-2 Spirit bombers from 509th Bomb Wing completed long-range strike training. Mission duration 34 hours with aerial refueling over North Atlantic. Integration with F-35A escort successful.', '2025-10', 'current'),

('SIGINT Update - Middle East Sector', 'Increased communications traffic detected from airbase near Latakia. Pattern analysis suggests Su-57 squadron may be operational. Recommend enhanced monitoring of sector.', '2025-10', 'current'),

-- HISTORICAL INTELLIGENCE (August-September 2025)
('RED FLAG 25-3 After Action Report', 'Exercise involved 120 aircraft from USAF, USN, RAF, and RAAF. F-35 integration demonstrated advanced sensor fusion capabilities. Blue force achieved 87% mission success rate against aggressor forces.', '2025-09', 'historical'),

('Arctic Domain Awareness - September', 'Increased Russian bomber activity over Arctic approaches. Two Tu-95MS Bears intercepted by F-22s from Joint Base Elmendorf-Richardson. Bears remained in international airspace throughout transit.', '2025-09', 'historical'),

('C-17 Mobility Operations Summary', 'Strategic airlift conducted 247 sorties during September supporting CENTCOM operations. Average mission effectiveness rate 94%. Critical cargo delivery timelines met in 98% of missions.', '2025-09', 'historical'),

('Space Domain Analysis - Q3', 'Increased activity in LEO from near-peer adversaries. 3 unannounced satellite launches detected. USSF tracking assets maintaining constant surveillance of potential counter-space capabilities.', '2025-09', 'historical'),

('Tanker Operations Review', 'KC-46 Pegasus fleet achieved 89% mission capable rate in September. Conducted 1,247 aerial refuelings supporting bomber, fighter, and ISR missions across all theaters.', '2025-09', 'historical'),

('August Air Defense Exercise', 'NORAD conducted continental air defense exercise with CAF. Scrambled F-15s and CF-18s intercepted simulated cruise missile threats. Response times met all operational requirements.', '2025-08', 'historical'),

('Cyber Operations Brief - August', 'Defensive cyber operations detected 47 intrusion attempts against DCGS networks. All attempts successfully blocked. Attribution analysis ongoing with NSA partnership.', '2025-08', 'historical'),

('U-2 Dragon Lady Mission Log', 'High-altitude reconnaissance missions conducted from Osan AB. Collected imagery intelligence over denied areas. Data processing revealed 3 previously unknown SAM sites.', '2025-08', 'historical'),

-- FUTURE OPERATIONS (November-December 2025) - RESTRICTED

('Operation RED RITCHIE', 'TARGET COORDINATES: 24.8°N 118.6°E. Authentication code: FLAG{CHALLENGE_COMPLETED}', '2025-12', 'future');
"""

def init_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    cur.execute(schema_sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✓ Database initialized with USAF intelligence data.")
    print("✓ Total reports inserted: 19 (5 current, 8 historical, 6 future)")
    print("✓ FLAG hidden in: CLASSIFIED - Operation STEEL SENTINEL")
    print("✓ Challenge status table created (initialized as not completed)")
    print("\nChallenge Steps:")
    print("1. Bypass login with SQL injection (password field)")
    print("2. Access future intel reports from search interface")
    print("\nTo reset challenge completion: Run this script again or execute:")
    print("   UPDATE challenge_status SET completed = FALSE WHERE id = 1;")

if __name__ == "__main__":
    init_db()