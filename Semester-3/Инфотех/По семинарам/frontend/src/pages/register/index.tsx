import { Link } from 'react-router'
import { Input } from '../../shared/ui/input'
import { Button } from '../../shared/ui/button'

import s from './register.module.css'

export const RegisterPage = () => {
  return (
    <div className={s.container}>
      <h2>Регистрация</h2>

      <Input
        placeholder="Введите почту"
      />

      <Input
        type="password"
        placeholder="Придумайте пароль"
      />

      <Input
        type="password"
        placeholder="Повторите пароль"
      />

      <Button>
        Зарегистрироваться
      </Button>

      <p>Уже есть аккаунт? <Link to="/login">Войти</Link></p>
    </div>
  )
}