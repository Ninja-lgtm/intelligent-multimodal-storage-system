"""
Database Manager for JSON Data Storage
Handles both SQL and NoSQL classified JSON data
"""

import sqlite3
import json
import os
from datetime import datetime

class JSONDatabaseManager:
    def __init__(self, storage_base='storage'):
        self.storage_base = storage_base
        self.db_path = os.path.join(storage_base, 'json_data.db')
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with tables for JSON storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for storing all JSON data entries
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS json_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                filename TEXT NOT NULL,
                storage_type TEXT NOT NULL,
                json_data TEXT NOT NULL,
                comment TEXT,
                uploaded_at TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table for storing flattened key-value pairs (for SQL-type data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS json_flat_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                data_type TEXT,
                FOREIGN KEY (entry_id) REFERENCES json_entries(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_json(self, username, filename, storage_type, json_data, comment=''):
        """Store JSON data in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Store main entry
            cursor.execute('''
                INSERT INTO json_entries 
                (username, filename, storage_type, json_data, comment, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                username,
                filename,
                storage_type,
                json.dumps(json_data),
                comment,
                datetime.now().isoformat()
            ))
            
            entry_id = cursor.lastrowid
            
            # If SQL type, also store flattened data
            if storage_type == 'sql':
                self._store_flattened_data(cursor, entry_id, json_data)
            
            conn.commit()
            return entry_id
        
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _store_flattened_data(self, cursor, entry_id, data, prefix=''):
        """Store flattened key-value pairs for SQL-type data"""
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, (dict, list)):
                    # Skip nested structures (shouldn't happen for SQL type)
                    continue
                else:
                    value_type = type(value).__name__
                    cursor.execute('''
                        INSERT INTO json_flat_data (entry_id, key, value, data_type)
                        VALUES (?, ?, ?, ?)
                    ''', (entry_id, full_key, str(value), value_type))
    
    def get_user_json_entries(self, username):
        """Retrieve all JSON entries for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, storage_type, json_data, comment, uploaded_at
            FROM json_entries
            WHERE username = ?
            ORDER BY uploaded_at DESC
        ''', (username,))
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                'id': row[0],
                'filename': row[1],
                'storage_type': row[2],
                'json_data': json.loads(row[3]),
                'comment': row[4],
                'uploaded_at': row[5]
            })
        
        conn.close()
        return entries
    
    def get_entry_by_id(self, entry_id, username):
        """Get specific JSON entry by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, storage_type, json_data, comment, uploaded_at
            FROM json_entries
            WHERE id = ? AND username = ?
        ''', (entry_id, username))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'filename': row[1],
                'storage_type': row[2],
                'json_data': json.loads(row[3]),
                'comment': row[4],
                'uploaded_at': row[5]
            }
        return None
    
    def get_flattened_data(self, entry_id):
        """Get flattened data for SQL-type entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT key, value, data_type
            FROM json_flat_data
            WHERE entry_id = ?
            ORDER BY key
        ''', (entry_id,))
        
        data = []
        for row in cursor.fetchall():
            data.append({
                'key': row[0],
                'value': row[1],
                'type': row[2]
            })
        
        conn.close()
        return data
    
    def delete_entry(self, entry_id, username):
        """Delete a JSON entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete flattened data first
            cursor.execute('DELETE FROM json_flat_data WHERE entry_id = ?', (entry_id,))
            
            # Delete main entry
            cursor.execute('''
                DELETE FROM json_entries 
                WHERE id = ? AND username = ?
            ''', (entry_id, username))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def search_entries(self, username, query='', storage_type=None):
        """Search JSON entries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = '''
            SELECT id, filename, storage_type, json_data, comment, uploaded_at
            FROM json_entries
            WHERE username = ?
        '''
        params = [username]
        
        if query:
            sql += ' AND (filename LIKE ? OR comment LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%'])
        
        if storage_type:
            sql += ' AND storage_type = ?'
            params.append(storage_type)
        
        sql += ' ORDER BY uploaded_at DESC'
        
        cursor.execute(sql, params)
        
        entries = []
        for row in cursor.fetchall():
            entries.append({
                'id': row[0],
                'filename': row[1],
                'storage_type': row[2],
                'json_data': json.loads(row[3]),
                'comment': row[4],
                'uploaded_at': row[5]
            })
        
        conn.close()
        return entries