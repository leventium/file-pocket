package interfaces

type NotFoundError struct {
	msg string
}

type InternalError struct {
	msg string
}

func NewNotFoundError(msg string) *NotFoundError {
	return &NotFoundError{msg: msg}
}

func (n *NotFoundError) Error() string {
	return n.msg
}

func NewInternalError(msg string) *InternalError {
	return &InternalError{msg: msg}
}

func (i *InternalError) Error() string {
	return i.msg
}
