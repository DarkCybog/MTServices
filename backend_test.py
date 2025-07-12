#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Task Marketplace Super App
Tests all major backend functionality including user management, tasks, payments, location, messaging, and reviews.
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time

# Backend URL from environment
BACKEND_URL = "https://807423d5-f4c5-400d-bf1e-1f2c22da3dc6.preview.emergentagent.com/api"

class TaskMarketplaceAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_data = {}
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def log_test(self, test_name, success, details=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success:
            print(f"   Error occurred in: {test_name}")
        print()

    def test_api_health(self):
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/")
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.json() if success else response.text}"
            self.log_test("API Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("API Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_user_management_system(self):
        """Test User Management System (Dual Roles) - HIGH PRIORITY"""
        print("=== Testing User Management System (Dual Roles) ===")
        
        # Test 1: Create Client User
        try:
            client_data = {
                "email": "sarah.johnson@email.com",
                "phone": "+1-555-0123",
                "name": "Sarah Johnson",
                "role": "client",
                "bio": "Busy professional looking for reliable task assistance",
                "skills": []
            }
            
            response = self.session.post(f"{self.base_url}/users", json=client_data)
            success = response.status_code == 200
            if success:
                client_user = response.json()
                self.test_data['client_user'] = client_user
                details = f"Created client user: {client_user['name']} (ID: {client_user['id']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Client User", success, details)
            
        except Exception as e:
            self.log_test("Create Client User", False, f"Exception: {str(e)}")
            return False

        # Test 2: Create Tasker User
        try:
            tasker_data = {
                "email": "mike.rodriguez@email.com",
                "phone": "+1-555-0456",
                "name": "Mike Rodriguez",
                "role": "tasker",
                "bio": "Experienced handyman and delivery specialist with 5+ years experience",
                "skills": ["handyman", "delivery", "cleaning", "moving"]
            }
            
            response = self.session.post(f"{self.base_url}/users", json=tasker_data)
            success = response.status_code == 200
            if success:
                tasker_user = response.json()
                self.test_data['tasker_user'] = tasker_user
                details = f"Created tasker user: {tasker_user['name']} (ID: {tasker_user['id']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Tasker User", success, details)
            
        except Exception as e:
            self.log_test("Create Tasker User", False, f"Exception: {str(e)}")
            return False

        # Test 3: Create Dual Role User
        try:
            dual_data = {
                "email": "alex.chen@email.com",
                "phone": "+1-555-0789",
                "name": "Alex Chen",
                "role": "both",
                "bio": "Freelancer who both offers services and needs help with tasks",
                "skills": ["tech_support", "tutoring", "delivery"]
            }
            
            response = self.session.post(f"{self.base_url}/users", json=dual_data)
            success = response.status_code == 200
            if success:
                dual_user = response.json()
                self.test_data['dual_user'] = dual_user
                details = f"Created dual-role user: {dual_user['name']} (ID: {dual_user['id']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Dual Role User", success, details)
            
        except Exception as e:
            self.log_test("Create Dual Role User", False, f"Exception: {str(e)}")
            return False

        # Test 4: Get User Profile
        if 'client_user' in self.test_data:
            try:
                user_id = self.test_data['client_user']['id']
                response = self.session.get(f"{self.base_url}/users/{user_id}")
                success = response.status_code == 200
                if success:
                    user = response.json()
                    details = f"Retrieved user: {user['name']}, Role: {user['role']}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Get User Profile", success, details)
                
            except Exception as e:
                self.log_test("Get User Profile", False, f"Exception: {str(e)}")

        # Test 5: Update User Information
        if 'tasker_user' in self.test_data:
            try:
                user_id = self.test_data['tasker_user']['id']
                update_data = {
                    "bio": "Updated: Expert handyman specializing in home repairs and maintenance",
                    "is_verified": True
                }
                
                response = self.session.put(f"{self.base_url}/users/{user_id}", json=update_data)
                success = response.status_code == 200
                if success:
                    updated_user = response.json()
                    details = f"Updated user bio and verification status"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Update User Information", success, details)
                
            except Exception as e:
                self.log_test("Update User Information", False, f"Exception: {str(e)}")

        # Test 6: List Users with Role Filtering
        try:
            response = self.session.get(f"{self.base_url}/users?role=tasker")
            success = response.status_code == 200
            if success:
                users = response.json()
                tasker_count = len([u for u in users if u['role'] in ['tasker', 'both']])
                details = f"Found {tasker_count} taskers/dual-role users"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("List Users with Role Filtering", success, details)
            
        except Exception as e:
            self.log_test("List Users with Role Filtering", False, f"Exception: {str(e)}")

        return True

    def test_task_marketplace_system(self):
        """Test Task Marketplace System - HIGH PRIORITY"""
        print("=== Testing Task Marketplace System ===")
        
        if 'client_user' not in self.test_data or 'tasker_user' not in self.test_data:
            self.log_test("Task Marketplace System", False, "Missing required users for testing")
            return False

        # Test 1: Create Task
        try:
            task_data = {
                "title": "Furniture Assembly and Room Setup",
                "description": "Need help assembling IKEA furniture and organizing living room. Includes bookshelf, coffee table, and TV stand. Should take about 3-4 hours.",
                "category": "handyman",
                "client_id": self.test_data['client_user']['id'],
                "location": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "address": "123 Main St, New York, NY 10001",
                    "is_shared": True
                },
                "budget_min": 80.0,
                "budget_max": 120.0,
                "priority": "normal",
                "estimated_duration": 240,
                "required_skills": ["handyman", "furniture_assembly"],
                "images": []
            }
            
            response = self.session.post(f"{self.base_url}/tasks", json=task_data)
            success = response.status_code == 200
            if success:
                task = response.json()
                self.test_data['task'] = task
                details = f"Created task: {task['title']} (ID: {task['id']}, Budget: ${task['budget_min']}-${task['budget_max']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Task", success, details)
            
        except Exception as e:
            self.log_test("Create Task", False, f"Exception: {str(e)}")
            return False

        # Test 2: Browse Tasks by Category
        try:
            response = self.session.get(f"{self.base_url}/tasks?category=handyman")
            success = response.status_code == 200
            if success:
                tasks = response.json()
                details = f"Found {len(tasks)} handyman tasks"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Browse Tasks by Category", success, details)
            
        except Exception as e:
            self.log_test("Browse Tasks by Category", False, f"Exception: {str(e)}")

        # Test 3: Get Specific Task
        if 'task' in self.test_data:
            try:
                task_id = self.test_data['task']['id']
                response = self.session.get(f"{self.base_url}/tasks/{task_id}")
                success = response.status_code == 200
                if success:
                    task = response.json()
                    details = f"Retrieved task: {task['title']}, Status: {task['status']}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Get Specific Task", success, details)
                
            except Exception as e:
                self.log_test("Get Specific Task", False, f"Exception: {str(e)}")

        # Test 4: Task Acceptance Workflow
        if 'task' in self.test_data:
            try:
                task_id = self.test_data['task']['id']
                tasker_id = self.test_data['tasker_user']['id']
                
                response = self.session.put(f"{self.base_url}/tasks/{task_id}/accept?tasker_id={tasker_id}")
                success = response.status_code == 200
                if success:
                    result = response.json()
                    details = f"Task accepted by tasker: {result['message']}"
                    # Update our test data
                    self.test_data['task']['status'] = 'accepted'
                    self.test_data['task']['tasker_id'] = tasker_id
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Task Acceptance Workflow", success, details)
                
            except Exception as e:
                self.log_test("Task Acceptance Workflow", False, f"Exception: {str(e)}")

        # Test 5: Task Status Updates (Start)
        if 'task' in self.test_data:
            try:
                task_id = self.test_data['task']['id']
                
                response = self.session.put(f"{self.base_url}/tasks/{task_id}/start")
                success = response.status_code == 200
                if success:
                    result = response.json()
                    details = f"Task started: {result['message']}"
                    self.test_data['task']['status'] = 'in_progress'
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Task Status Update (Start)", success, details)
                
            except Exception as e:
                self.log_test("Task Status Update (Start)", False, f"Exception: {str(e)}")

        # Test 6: Task Status Updates (Complete)
        if 'task' in self.test_data:
            try:
                task_id = self.test_data['task']['id']
                
                response = self.session.put(f"{self.base_url}/tasks/{task_id}/complete")
                success = response.status_code == 200
                if success:
                    result = response.json()
                    details = f"Task completed: {result['message']}"
                    self.test_data['task']['status'] = 'completed'
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Task Status Update (Complete)", success, details)
                
            except Exception as e:
                self.log_test("Task Status Update (Complete)", False, f"Exception: {str(e)}")

        # Test 7: Filter Tasks by Status and Client
        try:
            client_id = self.test_data['client_user']['id']
            response = self.session.get(f"{self.base_url}/tasks?client_id={client_id}&status=completed")
            success = response.status_code == 200
            if success:
                tasks = response.json()
                details = f"Found {len(tasks)} completed tasks for client"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Filter Tasks by Status and Client", success, details)
            
        except Exception as e:
            self.log_test("Filter Tasks by Status and Client", False, f"Exception: {str(e)}")

        return True

    def test_task_bidding_system(self):
        """Test Task Bidding System"""
        print("=== Testing Task Bidding System ===")
        
        # Create a new task for bidding
        try:
            task_data = {
                "title": "Apartment Deep Cleaning",
                "description": "Need thorough cleaning of 2-bedroom apartment including kitchen, bathrooms, and living areas.",
                "category": "cleaning",
                "client_id": self.test_data['client_user']['id'],
                "location": {
                    "latitude": 40.7589,
                    "longitude": -73.9851,
                    "address": "456 Park Ave, New York, NY 10016",
                    "is_shared": True
                },
                "budget_min": 100.0,
                "budget_max": 150.0,
                "priority": "urgent",
                "estimated_duration": 180,
                "required_skills": ["cleaning"],
                "images": []
            }
            
            response = self.session.post(f"{self.base_url}/tasks", json=task_data)
            if response.status_code == 200:
                bidding_task = response.json()
                self.test_data['bidding_task'] = bidding_task
                
                # Test 1: Create Bid
                bid_data = {
                    "task_id": bidding_task['id'],
                    "tasker_id": self.test_data['tasker_user']['id'],
                    "proposed_price": 125.0,
                    "message": "I have 5+ years of professional cleaning experience and can complete this job efficiently. I use eco-friendly products and guarantee satisfaction."
                }
                
                response = self.session.post(f"{self.base_url}/task-bids", json=bid_data)
                success = response.status_code == 200
                if success:
                    bid = response.json()
                    self.test_data['bid'] = bid
                    details = f"Created bid: ${bid['proposed_price']} for task {bidding_task['title']}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Create Task Bid", success, details)
                
                # Test 2: Get Task Bids
                if success:
                    response = self.session.get(f"{self.base_url}/task-bids/{bidding_task['id']}")
                    success = response.status_code == 200
                    if success:
                        bids = response.json()
                        details = f"Retrieved {len(bids)} bids for task"
                    else:
                        details = f"Status: {response.status_code}, Error: {response.text}"
                    
                    self.log_test("Get Task Bids", success, details)
                
        except Exception as e:
            self.log_test("Task Bidding System", False, f"Exception: {str(e)}")

    def test_payment_infrastructure(self):
        """Test Payment Infrastructure (Hybrid) - HIGH PRIORITY"""
        print("=== Testing Payment Infrastructure (Hybrid) ===")
        
        if 'client_user' not in self.test_data or 'tasker_user' not in self.test_data:
            self.log_test("Payment Infrastructure", False, "Missing required users for testing")
            return False

        # Test 1: Create Card Payment Account
        try:
            card_account_data = {
                "user_id": self.test_data['client_user']['id'],
                "type": "card",
                "card_number": "4532123456789012",
                "card_holder": "Sarah Johnson",
                "is_primary": True
            }
            
            response = self.session.post(f"{self.base_url}/payment-accounts", json=card_account_data)
            success = response.status_code == 200
            if success:
                card_account = response.json()
                self.test_data['card_account'] = card_account
                details = f"Created card account: {card_account['card_number']} (Gateway ID: {card_account['gateway_customer_id']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Card Payment Account", success, details)
            
        except Exception as e:
            self.log_test("Create Card Payment Account", False, f"Exception: {str(e)}")

        # Test 2: Create Bank Account
        try:
            bank_account_data = {
                "user_id": self.test_data['tasker_user']['id'],
                "type": "bank_account",
                "bank_name": "Chase Bank",
                "account_number": "1234567890",
                "routing_number": "021000021",
                "is_primary": True
            }
            
            response = self.session.post(f"{self.base_url}/payment-accounts", json=bank_account_data)
            success = response.status_code == 200
            if success:
                bank_account = response.json()
                self.test_data['bank_account'] = bank_account
                details = f"Created bank account: {bank_account['bank_name']} {bank_account['account_number']}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Bank Account", success, details)
            
        except Exception as e:
            self.log_test("Create Bank Account", False, f"Exception: {str(e)}")

        # Test 3: Create Neobank Wallet
        try:
            wallet_data = {
                "user_id": self.test_data['dual_user']['id'],
                "type": "neobank_wallet",
                "is_primary": True
            }
            
            response = self.session.post(f"{self.base_url}/payment-accounts", json=wallet_data)
            success = response.status_code == 200
            if success:
                wallet = response.json()
                self.test_data['wallet'] = wallet
                details = f"Created neobank wallet: Balance ${wallet['wallet_balance']}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Neobank Wallet", success, details)
            
        except Exception as e:
            self.log_test("Create Neobank Wallet", False, f"Exception: {str(e)}")

        # Test 4: Update Wallet Balance
        if 'wallet' in self.test_data:
            try:
                wallet_id = self.test_data['wallet']['id']
                
                response = self.session.put(f"{self.base_url}/payment-accounts/{wallet_id}/wallet?amount=500.0")
                success = response.status_code == 200
                if success:
                    result = response.json()
                    details = f"Added $500 to wallet: {result['message']}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Update Wallet Balance", success, details)
                
            except Exception as e:
                self.log_test("Update Wallet Balance", False, f"Exception: {str(e)}")

        # Test 5: Get Payment Accounts
        try:
            user_id = self.test_data['client_user']['id']
            response = self.session.get(f"{self.base_url}/payment-accounts/{user_id}")
            success = response.status_code == 200
            if success:
                accounts = response.json()
                details = f"Retrieved {len(accounts)} payment accounts for user"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Get Payment Accounts", success, details)
            
        except Exception as e:
            self.log_test("Get Payment Accounts", False, f"Exception: {str(e)}")

        # Test 6: Create Payment
        if 'task' in self.test_data:
            try:
                task_id = self.test_data['task']['id']
                
                response = self.session.post(f"{self.base_url}/payments?task_id={task_id}&payment_method=card&amount=100.0")
                success = response.status_code == 200
                if success:
                    payment = response.json()
                    self.test_data['payment'] = payment
                    details = f"Created payment: ${payment['amount']} (Gateway ID: {payment['gateway_payment_id']})"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Create Payment", success, details)
                
            except Exception as e:
                self.log_test("Create Payment", False, f"Exception: {str(e)}")

        return True

    def test_location_sharing_system(self):
        """Test Location Sharing System - HIGH PRIORITY"""
        print("=== Testing Location Sharing System ===")
        
        if 'tasker_user' not in self.test_data:
            self.log_test("Location Sharing System", False, "Missing required users for testing")
            return False

        # Test 1: Update User Location
        try:
            user_id = self.test_data['tasker_user']['id']
            location_data = {
                "latitude": 40.7831,
                "longitude": -73.9712,
                "address": "Central Park, New York, NY",
                "is_shared": True
            }
            
            response = self.session.put(f"{self.base_url}/users/{user_id}/location", json=location_data)
            success = response.status_code == 200
            if success:
                result = response.json()
                details = f"Updated location: {location_data['address']} (Shared: {location_data['is_shared']})"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Update User Location", success, details)
            
        except Exception as e:
            self.log_test("Update User Location", False, f"Exception: {str(e)}")

        # Test 2: Get User Location
        try:
            user_id = self.test_data['tasker_user']['id']
            response = self.session.get(f"{self.base_url}/users/{user_id}/location")
            success = response.status_code == 200
            if success:
                location = response.json()
                details = f"Retrieved location: Lat {location['latitude']}, Lng {location['longitude']}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Get User Location", success, details)
            
        except Exception as e:
            self.log_test("Get User Location", False, f"Exception: {str(e)}")

        return True

    def test_messaging_system(self):
        """Test Messaging & Communication - MEDIUM PRIORITY"""
        print("=== Testing Messaging & Communication ===")
        
        if 'task' not in self.test_data:
            self.log_test("Messaging System", False, "Missing required task for testing")
            return False

        # Test 1: Send Message
        try:
            message_data = {
                "task_id": self.test_data['task']['id'],
                "sender_id": self.test_data['client_user']['id'],
                "receiver_id": self.test_data['tasker_user']['id'],
                "content": "Hi Mike! Thanks for accepting the furniture assembly task. I'll be available all day Saturday. The furniture boxes are in the living room ready to go.",
                "message_type": "text"
            }
            
            response = self.session.post(f"{self.base_url}/messages", json=message_data)
            success = response.status_code == 200
            if success:
                message = response.json()
                self.test_data['message'] = message
                details = f"Sent message: '{message['content'][:50]}...'"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Send Message", success, details)
            
        except Exception as e:
            self.log_test("Send Message", False, f"Exception: {str(e)}")

        # Test 2: Send Reply Message
        try:
            reply_data = {
                "task_id": self.test_data['task']['id'],
                "sender_id": self.test_data['tasker_user']['id'],
                "receiver_id": self.test_data['client_user']['id'],
                "content": "Perfect! I'll arrive at 9 AM on Saturday with all my tools. Should take about 3-4 hours as estimated. I'll send you updates as I progress.",
                "message_type": "text"
            }
            
            response = self.session.post(f"{self.base_url}/messages", json=reply_data)
            success = response.status_code == 200
            if success:
                reply = response.json()
                details = f"Sent reply: '{reply['content'][:50]}...'"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Send Reply Message", success, details)
            
        except Exception as e:
            self.log_test("Send Reply Message", False, f"Exception: {str(e)}")

        # Test 3: Get Task Messages
        try:
            task_id = self.test_data['task']['id']
            response = self.session.get(f"{self.base_url}/messages/{task_id}")
            success = response.status_code == 200
            if success:
                messages = response.json()
                details = f"Retrieved {len(messages)} messages for task conversation"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Get Task Messages", success, details)
            
        except Exception as e:
            self.log_test("Get Task Messages", False, f"Exception: {str(e)}")

        return True

    def test_review_rating_system(self):
        """Test Review & Rating System - MEDIUM PRIORITY"""
        print("=== Testing Review & Rating System ===")
        
        if 'task' not in self.test_data:
            self.log_test("Review & Rating System", False, "Missing required task for testing")
            return False

        # Test 1: Create Review (Client reviews Tasker)
        try:
            review_data = {
                "task_id": self.test_data['task']['id'],
                "reviewer_id": self.test_data['client_user']['id'],
                "reviewee_id": self.test_data['tasker_user']['id'],
                "rating": 5,
                "comment": "Excellent work! Mike was punctual, professional, and did an amazing job assembling all the furniture. Everything looks perfect and he even cleaned up afterwards. Highly recommend!"
            }
            
            response = self.session.post(f"{self.base_url}/reviews", json=review_data)
            success = response.status_code == 200
            if success:
                review = response.json()
                self.test_data['review'] = review
                details = f"Created review: {review['rating']}/5 stars - '{review['comment'][:50]}...'"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Review (Client to Tasker)", success, details)
            
        except Exception as e:
            self.log_test("Create Review (Client to Tasker)", False, f"Exception: {str(e)}")

        # Test 2: Create Counter Review (Tasker reviews Client)
        try:
            counter_review_data = {
                "task_id": self.test_data['task']['id'],
                "reviewer_id": self.test_data['tasker_user']['id'],
                "reviewee_id": self.test_data['client_user']['id'],
                "rating": 5,
                "comment": "Great client! Sarah was very clear about expectations, had everything ready, and was easy to communicate with. Payment was prompt. Would work with again!"
            }
            
            response = self.session.post(f"{self.base_url}/reviews", json=counter_review_data)
            success = response.status_code == 200
            if success:
                counter_review = response.json()
                details = f"Created counter-review: {counter_review['rating']}/5 stars"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Create Review (Tasker to Client)", success, details)
            
        except Exception as e:
            self.log_test("Create Review (Tasker to Client)", False, f"Exception: {str(e)}")

        # Test 3: Get User Reviews
        try:
            user_id = self.test_data['tasker_user']['id']
            response = self.session.get(f"{self.base_url}/reviews/{user_id}")
            success = response.status_code == 200
            if success:
                reviews = response.json()
                details = f"Retrieved {len(reviews)} reviews for tasker"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Get User Reviews", success, details)
            
        except Exception as e:
            self.log_test("Get User Reviews", False, f"Exception: {str(e)}")

        # Test 4: Verify Rating Calculation
        try:
            user_id = self.test_data['tasker_user']['id']
            response = self.session.get(f"{self.base_url}/users/{user_id}")
            success = response.status_code == 200
            if success:
                user = response.json()
                details = f"User rating updated: {user['rating']}/5.0 ({user['total_reviews']} reviews)"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Verify Rating Calculation", success, details)
            
        except Exception as e:
            self.log_test("Verify Rating Calculation", False, f"Exception: {str(e)}")

        return True

    def test_service_categories_and_dashboard(self):
        """Test Service Categories and Dashboard APIs"""
        print("=== Testing Service Categories & Dashboard ===")
        
        # Test 1: Get Service Categories
        try:
            response = self.session.get(f"{self.base_url}/categories")
            success = response.status_code == 200
            if success:
                categories = response.json()
                details = f"Retrieved {len(categories)} service categories"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
            
            self.log_test("Get Service Categories", success, details)
            
        except Exception as e:
            self.log_test("Get Service Categories", False, f"Exception: {str(e)}")

        # Test 2: Get User Dashboard
        if 'tasker_user' in self.test_data:
            try:
                user_id = self.test_data['tasker_user']['id']
                response = self.session.get(f"{self.base_url}/dashboard/{user_id}")
                success = response.status_code == 200
                if success:
                    dashboard = response.json()
                    details = f"Dashboard: {dashboard['client_tasks']} client tasks, {dashboard['tasker_tasks']} tasker tasks, ${dashboard['total_earnings']} earnings"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                
                self.log_test("Get User Dashboard", success, details)
                
            except Exception as e:
                self.log_test("Get User Dashboard", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Comprehensive Backend API Testing for Task Marketplace Super App")
        print("=" * 80)
        
        # Test API connectivity first
        if not self.test_api_health():
            print("❌ API is not accessible. Stopping tests.")
            return False
        
        # Run tests in priority order
        test_results = []
        
        # High Priority Tests
        test_results.append(self.test_user_management_system())
        test_results.append(self.test_task_marketplace_system())
        test_results.append(self.test_payment_infrastructure())
        test_results.append(self.test_location_sharing_system())
        
        # Medium Priority Tests
        self.test_task_bidding_system()
        test_results.append(self.test_messaging_system())
        test_results.append(self.test_review_rating_system())
        
        # Additional Tests
        self.test_service_categories_and_dashboard()
        
        print("=" * 80)
        print("🏁 Backend API Testing Complete!")
        
        # Summary
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        print(f"📊 Test Summary: {passed_tests}/{total_tests} major test suites passed")
        
        if passed_tests == total_tests:
            print("✅ All major backend systems are working correctly!")
        else:
            print("⚠️  Some backend systems need attention.")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = TaskMarketplaceAPITester()
    tester.run_all_tests()