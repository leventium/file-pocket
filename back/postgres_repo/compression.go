package postgres_repo

import (
	"bytes"
	"compress/gzip"
	"file_pocket_back/models"
	"io"
)

func compress_file(file *models.File) error {
	var buff bytes.Buffer
	compressor, err := gzip.NewWriterLevel(&buff, 9)
	if err != nil {
		return err
	}
	_, err = compressor.Write(*file.Blob)
	if err != nil {
		return err
	}
	err = compressor.Close()
	if err != nil {
		return err
	}
	blob := buff.Bytes()
	file.Blob = &blob
	return nil
}

func decompress_file(blob *[]byte) error {
	blob_read := bytes.NewReader(*blob)
	decompressor, err := gzip.NewReader(blob_read)
	if err != nil {
		return err
	}
	file, err := io.ReadAll(decompressor)
	if err != nil {
		return err
	}
	err = decompressor.Close()
	if err != nil {
		return err
	}
	blob = &file
	return nil
}
