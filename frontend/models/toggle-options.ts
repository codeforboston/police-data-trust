export interface IToggleOptions {
  type: string
  value: boolean
}

export class ToggleOptions {
  options: IToggleOptions[] = []

  constructor(...args: string[]) {
    args.forEach((option, i) => {
      this.options.push({ type: option, value: i === 0 })
    })
  }
}
