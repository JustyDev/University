import {Link, useNavigate} from 'react-router'
import {Input} from '../../shared/ui/input'
import {Button} from '../../shared/ui/button'

import s from './login.module.css'
import {useUnit} from "effector-react";
import {initialQuery} from "../common/model.ts";
import {useEffect, useState} from "react";
import {loginQuery} from "./model.ts";
import {useQueryError} from "../../shared/hooks/useQueryError.ts";

export const LoginPage = () => {

  const { data } = useUnit(initialQuery)
  const navigate = useNavigate()

  useEffect(() => {
    if (data?.session) {
      navigate('/')
    }
  }, [data]);

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')

  const {pending} = useUnit(loginQuery)
  const {message} = useQueryError(loginQuery)

  return (
    <div className={s.container}>
      <h2>Вход в аккаунт</h2>

      <Input
        disabled={pending}
        onUpdate={setEmail}
        value={email}
        placeholder="Почта от аккаунта"
      />

      <Input
        disabled={pending}
        value={password}
        type="password"
        onUpdate={setPassword}
        placeholder="Пароль от аккаунта"
      />

      <Button disabled={pending} onClick={() => loginQuery.start({
        email,
        password
      })}>
        Войти в аккаунт
      </Button>

      {message && <p className={s.error}>Ошибка: {message}</p>}

      <p>Нет аккаунта? <Link to="/register">Регистрация</Link></p>
    </div>
  )
}