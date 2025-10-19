from app.models.habit import *
from app.models.hash import *
from app.utils.pagination import paginate_data
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.utils.router_utils import db_users, db_habits

router = APIRouter(prefix="/habits", tags=["Habits"])

# Cria hábito
@router.post("/", response_model=Habit, status_code=201)
async def create_habit(habit: HabitCreate):
    users = db_users.read()

    # Verifica se o usuário no id passado existe
    if not any(u['id'] == str(habit.user_id) for u in users):
        raise HTTPException(status_code=404, detail="User not found")

    habit_data = habit.model_dump()
    habit_data["creation_date"] = datetime.now()
    created_habit_data = db_habits.insert(habit_data)

    if not created_habit_data:
        raise HTTPException(detail="Failed to create habit", status_code=500)
    return Habit.model_validate(created_habit_data)

# Read de um habito inidividual
@router.get("/{habit_id}", response_model=Habit)
async def get_user(user_id: int):
    searched_habit = db_habits.read_one(user_id)
    if not searched_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return Habit.model_validate(searched_habit)

# Update
@router.put("/{habit_id}", response_model=HabitUpdate)
async def update_user(habit_id: int, habit: HabitUpdate):
    habit_update_data = habit.model_dump()

    updated_data = db_habits.update(habit_id, habit_update_data)

    if not updated_data:
        raise HTTPException(status_code=404, detail="Habit with id {habit_id} not found")
    return HabitUpdate.model_validate(updated_data)

# Delete
@router.delete("/{habit_id}", status_code=204)
async def delete_user(habit_id: int):
    success = db_habits.delete(habit_id);
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id: {habit_id} not found.")
    db_habits.vacuum()
    return

# Retorna página
@router.get("/", response_model=HabitsPaginationResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1)):
    all_habits = db_habits.read()
    return paginate_data(all_habits, page, page_size, Habit)
