from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, User, Task
from schemas import UserCreate, UserOut, UserUpdate, TaskCreate, TaskOut, TaskUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Task Manager API')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users', response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='email already exists')
    return new_user

@app.get('/users', response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id).all()

@app.get('/users/{user_id}', response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user

@app.put('/users/{user_id}', response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    user.name = payload.name
    user.email = payload.email
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail='email already exists')
    return user

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    db.delete(user)
    db.commit()
    return {'message': 'user deleted'}

@app.post('/tasks', response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=task.user_id,
    )
    db.add(new_task)
    try:
        db.commit()
        db.refresh(new_task)
    except IntegrityError as exc:
        db.rollback()
        if 'foreign key constraint' in str(exc).lower():
            raise HTTPException(status_code=400, detail='invalid user_id')
        raise
    return new_task

@app.get('/tasks', response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.id).all()

@app.get('/tasks/{task_id}', response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='task not found')
    return task

@app.put('/tasks/{task_id}', response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='task not found')
    task.title = payload.title
    task.description = payload.description
    task.status = payload.status
    task.user_id = payload.user_id
    try:
        db.commit()
        db.refresh(task)
    except IntegrityError as exc:
        db.rollback()
        if 'foreign key constraint' in str(exc).lower():
            raise HTTPException(status_code=400, detail='invalid user_id')
        raise
    return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='task not found')
    db.delete(task)
    db.commit()
    return {'message': 'task deleted'}
