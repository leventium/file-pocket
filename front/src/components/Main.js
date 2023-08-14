import React from 'react'
import Block_Selection from './Block_Selection'
import Load from './Load'
import Download from './Download'
import { useState } from 'react'

export default function Main() {
    const [flag, setFlag] = useState(false);
    const activeRegistrationClass = flag ? 'registration active' : 'registration';
    const activeFormBoxClass = flag ? 'form-box active' : 'form-box';
  return (
    <article className={activeRegistrationClass}>
        <div className='registration_container'> 
            <Block_Selection flag={flag} setFlag={setFlag} />
            <div className={activeFormBoxClass}>
                <Load />
                <Download />
            </div>
        </div>
    </article>
  )
}
