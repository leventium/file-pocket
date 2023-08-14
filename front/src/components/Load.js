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

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Файл не выбран");
      return;
    };
    
    setLoadKey('key001');
  };

  const uploadMore = async () => {
    setLoadKey(null);
  }

  return (
    <form action='#' className="form form_load">
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
