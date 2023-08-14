import React from 'react'
import useState from "react"

export default function Block_Selection(props) {

  return (
    <div className="block">
                <section className="block__item block-item">
                    <h2 className="block-item__title">Вы хотите загрузить файл?</h2>
                    <button onClick={() => {
                        props.setFlag(false);
                        }} 
                        className="block-item__btn signin-btn">
                        Загрузить
                    </button>
                </section>
                <section className="block__item block-item">
                    <h2 className="block-item__title">Вы хотите скачать файл?</h2>
                    <button onClick={() => {
                        props.setFlag(true);
                        }}
                        className="block-item__btn signup-btn">
                        Скачать
                    </button>
                </section>
    </div>
  )
}
