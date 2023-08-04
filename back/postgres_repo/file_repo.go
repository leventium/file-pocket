package postgres_repo

import (
	"context"
	"file_pocket_back/interfaces"
	"file_pocket_back/models"
	"file_pocket_back/postgres"
	"log"
)

type PostgresFileRepo struct {
	db *postgres.PostgresDatabase
}

func (p *PostgresFileRepo) Save(file *models.File) error {
	if err := compress_file(file); err != nil {
		log.Println("Compression error")
		return interfaces.NewInternalError("compressor error")
	}
	p.db.Mx.Lock()
	defer p.db.Mx.Unlock()

	_, err := p.db.GetConn().Exec(context.TODO(), `
		insert into files (id, filename, blob)
			values ($1, $2, $3)
		on conflict do update set
			filename = $2,
			blob = $3;
	`, file.Identifier, file.FileName, file.Blob)
	if err != nil {
		log.Println(err)
		return interfaces.NewInternalError("db error")
	}
	return nil
}

func (p *PostgresFileRepo) GetByIdentifier(id string) (*models.File, error) {
	p.db.Mx.Lock()

	var filename string
	var blob []byte

	err := p.db.GetConn().QueryRow(context.TODO(), `
		select filename, blob
		from files
		where id = $1;
	`).Scan(&filename, &blob)
	if err.Error() == "no rows in result set" {
		p.db.Mx.Unlock()
		return nil, interfaces.NewNotFoundError("not found")
	} else if err != nil {
		p.db.Mx.Unlock()
		return nil, interfaces.NewInternalError("db error")
	}
	p.db.Mx.Unlock()

	if err = decompress_file(&blob); err != nil {
		return nil, interfaces.NewInternalError("compression error")
	}
	return &models.File{
		Identifier: id,
		FileName:   filename,
		Blob:       &blob,
	}, nil
}

func (p *PostgresFileRepo) IsIdentifierBusy(id string) (bool, error) {
	p.db.Mx.Lock()
	defer p.db.Mx.Unlock()

	var count int

	err := p.db.GetConn().QueryRow(context.TODO(), `
		select count(*)
		from files
		where id = $1;
	`, id).Scan(&count)
	if err != nil {
		return false, interfaces.NewInternalError("db error")
	}

	return count > 0, nil
}

func (p *PostgresFileRepo) Delete(id string) error {
	p.db.Mx.Lock()
	defer p.db.Mx.Unlock()

	_, err := p.db.GetConn().Exec(context.TODO(), `
		delete from files
		where id = $1;
	`, id)
	if err != nil {
		return interfaces.NewInternalError("db error")
	}
	return nil
}
