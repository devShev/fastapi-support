from fastapi import APIRouter

router = APIRouter(
    prefix='/auth'
)


@router.get('/sign-up')
def sign_up():
    pass


@router.get('/sign-in')
def sign_in():
    pass
