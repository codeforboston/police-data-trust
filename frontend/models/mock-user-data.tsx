import {UserRoles} from './profile'

export const mockData = [
  {
    id: 1,
    active: true,
    firstName: 'Bob',
    lastName: 'Boberton',
    email: 'bob1@email.com',
    pwHash: '*****',
    phone: '9995559999',
    role: UserRoles.PUBLIC
  },
  {
    id: 2,
    active: true,
    firstName: 'Alice',
    lastName: 'Cooper',
    email: 'alice@email.com',
    pwHash: 'alsdkjf',
    phone: '9995559990',
    role: UserRoles.PASSPORT
  },
]
