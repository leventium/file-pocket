package service

type UserError struct {
	msg string
}

type InternalError struct {
	msg string
}

func NewUserError(msg string) *UserError {
	return &UserError{
		msg: msg,
	}
}

func (u *UserError) Error() string {
	return u.msg
}

func NewInternalError(msg string) *InternalError {
	return &InternalError{
		msg: msg,
	}
}

func (i *InternalError) Error() string {
	return i.msg
}
