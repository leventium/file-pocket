package interfaces

import "file_pocket_back/models"

type FileStorage interface {
	Save(file *models.File) error
	GetByIdentifier(id string) (*[]byte, error)
	Delete(id string) error
}
