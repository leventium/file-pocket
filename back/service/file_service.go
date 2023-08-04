package service

import (
	"errors"
	"file_pocket_back/interfaces"
	"file_pocket_back/models"
	"log"
	"math/rand"
	"strings"
)

type fileService struct {
	idLen    int
	fileRepo interfaces.FileRepo
}

var symbolRange = []byte(
	"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

func genRandString(n int) string {
	var sb strings.Builder
	sb.Grow(n)

	for i := 0; i < n; i++ {
		sb.WriteByte(symbolRange[rand.Intn(len(symbolRange))])
	}
	return sb.String()
}

func (s *fileService) PutFile(filename string, blob *[]byte) error {
	if len(filename) == 0 {
		log.Println("Got empty filename.")
		return NewUserError("filename mustn't be empty")
	}

	var id string
	for i := 0; i < 10; i++ {
		id = genRandString(s.idLen)
		if res, err := s.fileRepo.IsIdentifierBusy(id); err != nil {
			log.Println("Error occured while connecting to database.")
			return NewInternalError("internal error")
		} else if !res {
			break
		}
	}

	file := models.NewFile(id, filename, blob)
	err := s.fileRepo.Save(&file)
	if err != nil {
		return NewInternalError("internal error")
	}
	return nil
}

func handleRepoError(err error) error {
	var internalErr *interfaces.InternalError
	var notFoundErr *interfaces.NotFoundError

	switch {
	case errors.As(err, &internalErr):
		return NewInternalError("internal error")
	case errors.As(err, &notFoundErr):
		return NewUserError(notFoundErr.Error())
	default:
		return errors.New("unknown error occured")
	}
}

func (s *fileService) GetFile(id string) (string, *[]byte, error) {
	file, err := s.fileRepo.GetByIdentifier(id)
	if err != nil {
		return "", &[]byte{}, handleRepoError(err)
	}
	return file.FileName, file.Blob, nil
}
