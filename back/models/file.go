package models

type File struct {
	Identifier string
	FileName   string
	Blob       *[]byte
}

func NewFile(id, name string, blob *[]byte) File {
	return File{
		Identifier: id,
		FileName:   name,
		Blob:       blob,
	}
}
