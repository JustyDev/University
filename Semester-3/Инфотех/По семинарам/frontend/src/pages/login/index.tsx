import { Link } from 'react-router'
import { Input } from '../../shared/ui/input'
import { Button } from '../../shared/ui/button'

import s from './login.module.css'

export const LoginPage = () => {
  return (
    <div className={s.container}>
      <h2>Вход в аккаунт</h2>

      <Input
        placeholder="Почта от аккаунта"
      />

      <Input
        type="password"
        placeholder="Пароль от аккаунта"
      />

      <Button>
        Войти в аккаунт
      </Button>

      <p>Нет аккаунта? <Link to="/register">Регистрация</Link></p>
    </div>
  )
}