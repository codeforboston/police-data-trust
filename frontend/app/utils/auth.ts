const TOKEN_NAME = 'access_token';

export const isLoggedIn : boolean = !!localStorage.getItem(TOKEN_NAME);

export const removeAuthToken = (): void => {
  localStorage.removeItem(TOKEN_NAME);
}

export const setAuthToken = (token: string): void => {
  localStorage.setItem(TOKEN_NAME, token);
}