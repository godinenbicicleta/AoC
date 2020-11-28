defmodule House do
  def run(goal) do
    run(1, goal, 0)
  end

  def run(hn, goal, goal) do
    IO.puts("here")
    hn - 1
  end

  def run(hn, goal, _total) do
    fs = get_divisors(hn)

    factors =
      if hn > 1 do
        [1, hn | fs]
      else
        [1 | fs]
      end

    res = Enum.sum(factors) * 10

    IO.puts("house #{hn} got #{res}")

    if res >= goal do
      hn
    else
      run(hn + 1, goal, res)
    end
  end

  def get_divisors(num) do
    get_divisors(num, 2, :math.sqrt(num), [])
  end

  def get_divisors(_num, candidate, top, res) when top < candidate do
    res
  end

  def get_divisors(num, candidate, top, res) do
    case rem(num, candidate) do
      0 ->
        if div(num, candidate) != candidate do
          get_divisors(num, candidate + 1, top, [div(num, candidate), candidate | res])
        else
          get_divisors(num, candidate + 1, top, [candidate | res])
        end

      _k ->
        get_divisors(num, candidate + 1, top, res)
    end
  end
end

[10, 30, 40, 70, 60, 120, 80, 150, 130]
|> Enum.map(&House.run/1)
|> IO.inspect()

# too high: 2259441
House.run(34_000_000)
|> IO.inspect()
