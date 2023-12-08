defmodule Day08 do
  def p1 do
    {instructions, map} = preprocess("data/day08.txt")

    Enum.reduce_while(instructions, {"AAA", 0}, &reducer1(&1, &2, map))
  end

  def p2 do
    {instructions, map} = preprocess("data/day08.txt")

    starts = map |> Map.keys() |> Enum.filter(&String.ends_with?(&1, "A"))

    res = Enum.zip(starts, Stream.cycle([%{}])) |> Enum.into(%{})
    starts = Enum.zip(starts, starts) |> Enum.into(%{})

    Enum.reduce_while(instructions, {starts, 0, res}, &reducer2(&1, &2, map))
    |> to_result
  end

  def to_result(map) do
    nums =
      map
      |> Map.values()
      |> Enum.map(&Map.values/1)
      |> Enum.map(&hd/1)
      |> Enum.map(fn [a, b | _rest] -> a - b end)

    max_num = div(Enum.max(nums), 2)

    primes =
      Stream.iterate(2, &(&1 + 1))
      |> Stream.filter(&is_prime/1)
      |> Enum.take_while(&(&1 <= max_num))

    mcm(nums, primes)
  end

  def mcm(nums, primes) do
    nums
    |> Enum.map(&factors(&1, primes))
    |> Enum.reduce(
      %{},
      fn m, acc ->
        Map.merge(m, acc, fn _k, v1, v2 -> max(v1, v2) end)
      end
    )
    |> Enum.reduce(1, fn {num, exp}, acc -> acc * num ** exp end)
  end

  def is_prime(n) do
    Stream.iterate(2, &(&1 + 1))
    |> Enum.take_while(fn x -> x < n end)
    |> Enum.all?(fn x -> rem(n, x) > 0 end)
  end

  def factors(num, primes) do
    Enum.filter(primes, fn p -> rem(num, p) == 0 and p <= num end)
    |> Enum.map(fn p -> {p, to_exp(p, num, 0)} end)
    |> Enum.into(%{})
  end

  def to_exp(prime, num, acc) do
    if rem(num, prime) == 0 do
      to_exp(prime, div(num, prime), acc + 1)
    else
      acc
    end
  end

  def preprocess(fname) do
    [instructions, _blank | lines] =
      File.stream!(fname)
      |> Enum.to_list()

    instructions =
      String.trim(instructions)
      |> String.codepoints()
      |> Stream.cycle()

    map =
      lines
      |> Enum.map(&parse/1)
      |> Enum.into(%{})

    {instructions, map}
  end

  def reducer2(instruction, {currents, steps, res}, map) do
    res =
      Enum.map(res, fn {key, zmap} ->
        if String.ends_with?(currents[key], "Z") do
          {key, Map.update(zmap, currents[key], [], fn old -> [steps | old] end)}
        else
          {key, zmap}
        end
      end)
      |> Enum.into(%{})

    if Enum.all?(res, fn {_, zmap} ->
         map_size(zmap) > 0 and Enum.all?(zmap, fn {_, v} -> length(v) > 1 end)
       end) do
      {:halt, res}
    else
      currents =
        case instruction do
          "R" ->
            Enum.map(currents, fn {start, x} -> {start, map[x]["right"]} end) |> Enum.into(%{})

          "L" ->
            Enum.map(currents, fn {start, x} -> {start, map[x]["left"]} end) |> Enum.into(%{})
        end

      {:cont, {currents, steps + 1, res}}
    end
  end

  def reducer1(_, {"ZZZ", steps}, _), do: {:halt, steps}

  def reducer1(instruction, {current, steps}, map) do
    next =
      case instruction do
        "R" -> map[current]["right"]
        "L" -> map[current]["left"]
      end

    {:cont, {next, steps + 1}}
  end

  def parse(line) do
    [key, rules] = String.split(line, " = ")

    val = Regex.named_captures(~r/\((?<left>\w+), (?<right>\w+)\)/, rules)
    {key, val}
  end
end
