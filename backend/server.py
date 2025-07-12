from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from enum import Enum
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enums
class UserRole(str, Enum):
    CLIENT = "client"
    TASKER = "tasker"
    BOTH = "both"

class TaskStatus(str, Enum):
    POSTED = "posted"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class PaymentMethod(str, Enum):
    CARD = "card"
    BANK_ACCOUNT = "bank_account"
    NEOBANK_WALLET = "neobank_wallet"

class TaskCategory(str, Enum):
    DELIVERY = "delivery"
    CLEANING = "cleaning"
    HANDYMAN = "handyman"
    MOVING = "moving"
    BEAUTY = "beauty"
    TECH_SUPPORT = "tech_support"
    TUTORING = "tutoring"
    PET_CARE = "pet_care"
    TRANSPORTATION = "transportation"
    OTHER = "other"

# Models
class LocationModel(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    is_shared: bool = False

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    phone: str
    name: str
    role: UserRole
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    location: Optional[LocationModel] = None
    rating: float = 0.0
    total_reviews: int = 0
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserCreate(BaseModel):
    email: str
    phone: str
    name: str
    role: UserRole
    bio: Optional[str] = None
    skills: List[str] = Field(default_factory=list)

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: TaskCategory
    client_id: str
    tasker_id: Optional[str] = None
    location: LocationModel
    budget_min: float
    budget_max: float
    status: TaskStatus = TaskStatus.POSTED
    priority: str = "normal"  # normal, urgent, scheduled
    estimated_duration: Optional[int] = None  # in minutes
    required_skills: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)  # base64 encoded images
    scheduled_time: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str
    description: str
    category: TaskCategory
    client_id: str
    location: LocationModel
    budget_min: float
    budget_max: float
    priority: str = "normal"
    estimated_duration: Optional[int] = None
    required_skills: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)
    scheduled_time: Optional[datetime] = None

class TaskBid(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    tasker_id: str
    proposed_price: float
    message: str
    estimated_completion: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskBidCreate(BaseModel):
    task_id: str
    tasker_id: str
    proposed_price: float
    message: str
    estimated_completion: Optional[datetime] = None

class PaymentAccount(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    type: PaymentMethod
    # Card details (placeholder structure)
    card_number: Optional[str] = None  # "xxxx-xxxx-xxxx-1234" (masked)
    card_holder: Optional[str] = None
    # Bank account details (placeholder structure)
    bank_name: Optional[str] = None
    account_number: Optional[str] = None  # masked
    routing_number: Optional[str] = None
    # Neobank wallet
    wallet_balance: float = 0.0
    is_primary: bool = False
    gateway_customer_id: Optional[str] = None  # "xxxx-enter-gateway-api-here-xxxx"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentAccountCreate(BaseModel):
    user_id: str
    type: PaymentMethod
    card_number: Optional[str] = None
    card_holder: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    routing_number: Optional[str] = None
    is_primary: bool = False

class Payment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    client_id: str
    tasker_id: str
    amount: float
    payment_method: PaymentMethod
    gateway_payment_id: str = "xxxx-enter-gateway-api-here-xxxx"
    status: str = "pending"  # pending, completed, failed, refunded
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    reviewer_id: str
    reviewee_id: str
    rating: int  # 1-5
    comment: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewCreate(BaseModel):
    task_id: str
    reviewer_id: str
    reviewee_id: str
    rating: int
    comment: str

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    sender_id: str
    receiver_id: str
    content: str
    message_type: str = "text"  # text, image, location
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MessageCreate(BaseModel):
    task_id: str
    sender_id: str
    receiver_id: str
    content: str
    message_type: str = "text"

# User Management APIs
@api_router.post("/users", response_model=User)
async def create_user(user_data: UserCreate):
    user_dict = user_data.dict()
    user_obj = User(**user_dict)
    await db.users.insert_one(user_obj.dict())
    return user_obj

@api_router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@api_router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_data: Dict[str, Any]):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.users.update_one({"id": user_id}, {"$set": user_data})
    updated_user = await db.users.find_one({"id": user_id})
    return User(**updated_user)

@api_router.get("/users", response_model=List[User])
async def get_users(role: Optional[UserRole] = None, skills: Optional[str] = None):
    query = {}
    if role:
        query["role"] = role
    if skills:
        query["skills"] = {"$in": [skills]}
    
    users = await db.users.find(query).to_list(100)
    return [User(**user) for user in users]

# Task Management APIs
@api_router.post("/tasks", response_model=Task)
async def create_task(task_data: TaskCreate):
    task_dict = task_data.dict()
    task_obj = Task(**task_dict)
    await db.tasks.insert_one(task_obj.dict())
    return task_obj

@api_router.get("/tasks", response_model=List[Task])
async def get_tasks(
    category: Optional[TaskCategory] = None,
    status: Optional[TaskStatus] = None,
    client_id: Optional[str] = None,
    tasker_id: Optional[str] = None
):
    query = {}
    if category:
        query["category"] = category
    if status:
        query["status"] = status
    if client_id:
        query["client_id"] = client_id
    if tasker_id:
        query["tasker_id"] = tasker_id
    
    tasks = await db.tasks.find(query).sort("created_at", -1).to_list(100)
    return [Task(**task) for task in tasks]

@api_router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(**task)

@api_router.put("/tasks/{task_id}/accept")
async def accept_task(task_id: str, tasker_id: str):
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task["status"] != TaskStatus.POSTED:
        raise HTTPException(status_code=400, detail="Task is not available for acceptance")
    
    await db.tasks.update_one(
        {"id": task_id}, 
        {"$set": {"tasker_id": tasker_id, "status": TaskStatus.ACCEPTED, "accepted_at": datetime.utcnow()}}
    )
    return {"message": "Task accepted successfully"}

@api_router.put("/tasks/{task_id}/start")
async def start_task(task_id: str):
    await db.tasks.update_one(
        {"id": task_id}, 
        {"$set": {"status": TaskStatus.IN_PROGRESS, "started_at": datetime.utcnow()}}
    )
    return {"message": "Task started"}

@api_router.put("/tasks/{task_id}/complete")
async def complete_task(task_id: str):
    await db.tasks.update_one(
        {"id": task_id}, 
        {"$set": {"status": TaskStatus.COMPLETED, "completed_at": datetime.utcnow()}}
    )
    return {"message": "Task completed"}

# Task Bidding APIs
@api_router.post("/task-bids", response_model=TaskBid)
async def create_task_bid(bid_data: TaskBidCreate):
    bid_dict = bid_data.dict()
    bid_obj = TaskBid(**bid_dict)
    await db.task_bids.insert_one(bid_obj.dict())
    return bid_obj

@api_router.get("/task-bids/{task_id}", response_model=List[TaskBid])
async def get_task_bids(task_id: str):
    bids = await db.task_bids.find({"task_id": task_id}).sort("created_at", -1).to_list(100)
    return [TaskBid(**bid) for bid in bids]

# Payment Management APIs
@api_router.post("/payment-accounts", response_model=PaymentAccount)
async def create_payment_account(account_data: PaymentAccountCreate):
    account_dict = account_data.dict()
    
    # Mask sensitive data and add placeholder gateway integration
    if account_dict.get("card_number"):
        account_dict["card_number"] = f"****-****-****-{account_dict['card_number'][-4:]}"
    if account_dict.get("account_number"):
        account_dict["account_number"] = f"****{account_dict['account_number'][-4:]}"
    
    account_dict["gateway_customer_id"] = "xxxx-enter-gateway-api-here-xxxx"
    
    account_obj = PaymentAccount(**account_dict)
    await db.payment_accounts.insert_one(account_obj.dict())
    return account_obj

@api_router.get("/payment-accounts/{user_id}", response_model=List[PaymentAccount])
async def get_payment_accounts(user_id: str):
    accounts = await db.payment_accounts.find({"user_id": user_id}).to_list(100)
    return [PaymentAccount(**account) for account in accounts]

@api_router.put("/payment-accounts/{account_id}/wallet")
async def update_wallet_balance(account_id: str, amount: float):
    await db.payment_accounts.update_one(
        {"id": account_id, "type": PaymentMethod.NEOBANK_WALLET},
        {"$inc": {"wallet_balance": amount}}
    )
    return {"message": "Wallet balance updated"}

@api_router.post("/payments", response_model=Payment)
async def create_payment(task_id: str, payment_method: PaymentMethod, amount: float):
    task = await db.tasks.find_one({"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    payment_obj = Payment(
        task_id=task_id,
        client_id=task["client_id"],
        tasker_id=task["tasker_id"],
        amount=amount,
        payment_method=payment_method,
        gateway_payment_id="xxxx-enter-gateway-api-here-xxxx",
        status="pending"
    )
    
    await db.payments.insert_one(payment_obj.dict())
    return payment_obj

# Location Sharing APIs
@api_router.put("/users/{user_id}/location")
async def update_user_location(user_id: str, location: LocationModel):
    await db.users.update_one(
        {"id": user_id}, 
        {"$set": {"location": location.dict()}}
    )
    return {"message": "Location updated"}

@api_router.get("/users/{user_id}/location")
async def get_user_location(user_id: str):
    user = await db.users.find_one({"id": user_id}, {"location": 1})
    if not user or not user.get("location"):
        raise HTTPException(status_code=404, detail="Location not found")
    return user["location"]

# Messaging APIs
@api_router.post("/messages", response_model=Message)
async def send_message(message_data: MessageCreate):
    message_dict = message_data.dict()
    message_obj = Message(**message_dict)
    await db.messages.insert_one(message_obj.dict())
    return message_obj

@api_router.get("/messages/{task_id}", response_model=List[Message])
async def get_task_messages(task_id: str):
    messages = await db.messages.find({"task_id": task_id}).sort("created_at", 1).to_list(100)
    return [Message(**message) for message in messages]

# Review System APIs
@api_router.post("/reviews", response_model=Review)
async def create_review(review_data: ReviewCreate):
    review_dict = review_data.dict()
    review_obj = Review(**review_dict)
    await db.reviews.insert_one(review_obj.dict())
    
    # Update user rating
    user_reviews = await db.reviews.find({"reviewee_id": review_data.reviewee_id}).to_list(1000)
    total_rating = sum([review["rating"] for review in user_reviews])
    avg_rating = total_rating / len(user_reviews) if user_reviews else 0
    
    await db.users.update_one(
        {"id": review_data.reviewee_id},
        {"$set": {"rating": avg_rating, "total_reviews": len(user_reviews)}}
    )
    
    return review_obj

@api_router.get("/reviews/{user_id}", response_model=List[Review])
async def get_user_reviews(user_id: str):
    reviews = await db.reviews.find({"reviewee_id": user_id}).sort("created_at", -1).to_list(100)
    return [Review(**review) for review in reviews]

# Service Categories API
@api_router.get("/categories")
async def get_service_categories():
    categories = [
        {"id": "delivery", "name": "Delivery & Courier", "icon": "🚚"},
        {"id": "cleaning", "name": "Cleaning Services", "icon": "🧽"},
        {"id": "handyman", "name": "Handyman & Repairs", "icon": "🔧"},
        {"id": "moving", "name": "Moving & Lifting", "icon": "📦"},
        {"id": "beauty", "name": "Beauty & Wellness", "icon": "💄"},
        {"id": "tech_support", "name": "Tech Support", "icon": "💻"},
        {"id": "tutoring", "name": "Tutoring & Teaching", "icon": "📚"},
        {"id": "pet_care", "name": "Pet Care", "icon": "🐕"},
        {"id": "transportation", "name": "Transportation", "icon": "🚗"},
        {"id": "other", "name": "Other Services", "icon": "⚡"}
    ]
    return categories

# Analytics & Dashboard APIs
@api_router.get("/dashboard/{user_id}")
async def get_user_dashboard(user_id: str):
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's tasks based on their role
    if user["role"] in [UserRole.CLIENT, UserRole.BOTH]:
        client_tasks = await db.tasks.find({"client_id": user_id}).to_list(100)
    else:
        client_tasks = []
    
    if user["role"] in [UserRole.TASKER, UserRole.BOTH]:
        tasker_tasks = await db.tasks.find({"tasker_id": user_id}).to_list(100)
    else:
        tasker_tasks = []
    
    # Get earnings for taskers
    earnings = 0
    if user["role"] in [UserRole.TASKER, UserRole.BOTH]:
        payments = await db.payments.find({"tasker_id": user_id, "status": "completed"}).to_list(100)
        earnings = sum([payment["amount"] for payment in payments])
    
    return {
        "user": user,
        "client_tasks": len(client_tasks),
        "tasker_tasks": len(tasker_tasks),
        "total_earnings": earnings,
        "rating": user.get("rating", 0),
        "total_reviews": user.get("total_reviews", 0)
    }

# Basic API
@api_router.get("/")
async def root():
    return {"message": "Task Marketplace Super App API"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()