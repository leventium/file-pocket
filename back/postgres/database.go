package postgres

import (
	"context"
	"sync"

	"github.com/jackc/pgx/v5"
)

type PostgresDatabase struct {
	conn *pgx.Conn
	Mx   sync.Mutex
}

var inst *PostgresDatabase = nil
var mx sync.Mutex

func New(connString string) (*PostgresDatabase, error) {
	if inst == nil {
		mx.Lock()
		defer mx.Unlock()
		if inst == nil {
			conn, err := pgx.Connect(context.TODO(), connString)
			if err != nil {
				return nil, err
			}
			inst = &PostgresDatabase{conn: conn}
			err = inst.init()
			if err != nil {
				return nil, err
			}
		}
	}
	return inst, nil
}

func (p *PostgresDatabase) init() error {
	p.Mx.Lock()
	defer p.Mx.Unlock()

	_, err := p.conn.Exec(context.TODO(), `
		create table if not exists files (
			id			varchar(20) primary key,
			filename	varchar(100) not null,
			blob		bytea
		)
	`)
	return err
}

func (p *PostgresDatabase) GetConn() *pgx.Conn {
	return p.conn
}

func (p *PostgresDatabase) Close() error {
	inst = nil
	return p.conn.Close(context.TODO())
}
