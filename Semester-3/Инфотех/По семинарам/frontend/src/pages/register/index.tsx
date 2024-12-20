import {Link} from 'react-router'
import {Input} from '../../shared/ui/input'
import {Button} from '../../shared/ui/button'

import s from './register.module.css'
import {useUnit} from "effector-react/effector-react.umd";
import {registerQuery} from "./model.ts";
import {useQueryError} from "../../shared/hooks/useQueryError.ts";
import {useState} from "react";

export const RegisterPage = () => {

  const {data, pending} = useUnit(registerQuery)
  const {message: messageError} = useQueryError(registerQuery)

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [confirm, setConfirm] = useState<string>('')

  return (
    <div className={s.container}>
      <h2>Регистрация</h2>

      {data?.type === 'success' && <p>Успешная регистрация</p>}

      <Input
        value={email}
        onUpdate={setEmail}
        disabled={pending}
        placeholder="Введите почту"
      />

      <Input
        value={password}
        onUpdate={setPassword}
        disabled={pending}
        type="password"
        placeholder="Придумайте пароль"
      />

      <Input
        value={confirm}
        onUpdate={setConfirm}
        disabled={pending}
        type="password"
        placeholder="Повторите пароль"
      />

      <Button onClick={() => registerQuery.start({
        email: email,
        password: password,
        confirm_password: confirm
      })}>
        Зарегистрироваться
      </Button>

      {messageError && <p>Ошибка: {messageError}</p>}

      <p>Уже есть аккаунт? <Link to="/login">Войти</Link></p>
    </div>
  )
}