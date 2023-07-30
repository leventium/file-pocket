package interfaces

import "file_pocket_back/models"

type FileRepo interface {
	Save(file *models.File) error
	GetByIdentifier(id string) (*models.File, error)
	IsIdentifierBusy(id string) (bool, error)
	Delete(id string) error
}
