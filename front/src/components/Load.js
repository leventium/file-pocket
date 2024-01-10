import React from 'react';
import { useState } from 'react';

export default function Load() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loadKey, setLoadKey] = useState(null);

  const hFormTitleClass = loadKey ? "form-title hidden" : "form-title";
  const inputFileClass = loadKey ? "form_input hidden" : "form_input";
  const btnUploadClass = loadKey ? "form__btn hidden" : "form__btn";
  const keyTitleClass = loadKey ? "key-title" : "key-title hidden";
  const keyClass = loadKey ? "key" : "key hidden";
  const btnOneMoreLoadClass = loadKey ? "form__btn" : "form__btn hidden";

  const handleChange = (event) => {
    console.log(event.target.files);
    setSelectedFile(event.target.files[0])
  };

  const handleUpload = async (e) => {
    if (!selectedFile) {
      alert("Файл не выбран");
      return;
    };

    e.preventDefault();

  try {
    let response = await fetch('https://restcountries.com/v4.1/all', {
      method: 'POST',
      body: new FormData(formFile)
    });

    let data = response.json();

    if (response.ok) {
      alert("Файл отправлен");
      setLoadKey(data.file_id);
    }
    else if (response.status === 400) {
      alert("Ошибка! Файл слишком большой, допустимый размер файла не больше: " + data.file_maxsize + "; Размер вашего файла: " + data.recieved_size);
    }
    else if (response.status === 422) {
      alert("Ошибка!: невалидные данные");
    }
    else {
      alert("Ошибка " + response.status);
    }
  } catch (error) {
    console.log("Возникла проблема с вашим fetch запросом: ", error.message);
    alert("Возникла проблема с вашим fetch запросом: ", error.message);
  };
  };

  const uploadMore = async () => {
    setLoadKey('key002');
  }

  return (
    <form action='#' id="formFile" className="form form_load">
                    <h3 className={hFormTitleClass}>Загрузка файла</h3>
                    <p>
                        <input type="file" onChange={handleChange} className={inputFileClass} placeholder="Загрузить файл" />
                    </p>
                    <p>
                        <button onClick={handleUpload} className={btnUploadClass}>Сохранить</button>
                    </p>
                    <h3 className={keyTitleClass}>Ваш ключ:</h3>
                    <p className={keyClass}>{loadKey}</p>
                    <p>
                        <button onClick={uploadMore} className={btnOneMoreLoadClass}>Загрузить еще</button>
                    </p>
    </form>
  )
}
