import {useNavigate} from "react-router";
import {useEffect} from "react";
import {useUnit} from "effector-react";
import {initialQuery, logoutQuery} from "./model.ts";
import {Button} from "../../shared/ui/button";

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

  return (
    !pending && <div>
        Основная страница, которая появляется только если чел автолризован

        <Button onClick={() => logoutQuery.start()}>
            Выйти из аккаунта
        </Button>
    </div>
  )
}