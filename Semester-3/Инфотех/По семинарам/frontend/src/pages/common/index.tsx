import {NavLink, useNavigate} from "react-router";
import {useEffect, useState} from "react";
import {useUnit} from "effector-react";
import {initialQuery, logoutQuery, updateUserQuery} from "./model.ts";
import {Button} from "../../shared/ui/button";

import s from './common.module.css'
import {Input} from "../../shared/ui/input";

export const CommonPage = () => {

  const {data, pending} = useUnit(initialQuery)

  const navigate = useNavigate()

  useEffect(() => {
    if (!pending && data) {
      if (!data?.session) {
        navigate('/login')
      }
    }
  }, [pending, data])

  const [name, setName] = useState<string>('')
  const [surname, setSurname] = useState<string>('')

  const {pending: pendingUpdate} = useUnit(updateUserQuery)

  useEffect(() => {
    if (data?.session?.user) {
      setName(data?.session?.user?.name ?? '')
      setSurname(data?.session?.user?.surname ?? '')
    }
  }, [data?.session])

  return (
    !pending && data && <div>

        <nav className={s.nav}>
            <h3>Project</h3>
            <div>
                <NavLink to='/'>Мой аккаунт</NavLink>
            </div>
        </nav>

        <div className={s.wrapper}>
            <h2>Мой аккаунт</h2>

            <p>Имя</p>
            <Input
                disabled={pendingUpdate}
                value={name}
                onUpdate={setName}
                placeholder='Можете установить имя'
            />

            <p>Фамилия</p>
            <Input
                disabled={pendingUpdate}
                value={surname}
                onUpdate={setSurname}
                placeholder='Можете установить фамилию'
            />

            <br/>
            <br/>

          {name && name !== data?.session?.user?.name || surname && surname !== data?.session?.user?.surname ? (
            <Button disabled={pendingUpdate} onClick={() => updateUserQuery.start({
              name, surname
            })}>
              Применить изменения
            </Button>
          ) : null}

            <br/>
            <br/>

            <Button onClick={() => logoutQuery.start()}>
                Выйти из аккаунта
            </Button>
        </div>
    </div>
  )
}