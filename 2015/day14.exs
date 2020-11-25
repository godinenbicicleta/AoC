defmodule Reno do
  @content """
  Vixen can fly 8 km/s for 8 seconds, but then must rest for 53 seconds.
  Blitzen can fly 13 km/s for 4 seconds, but then must rest for 49 seconds.
  Rudolph can fly 20 km/s for 7 seconds, but then must rest for 132 seconds.
  Cupid can fly 12 km/s for 4 seconds, but then must rest for 43 seconds.
  Donner can fly 9 km/s for 5 seconds, but then must rest for 38 seconds.
  Dasher can fly 10 km/s for 4 seconds, but then must rest for 37 seconds.
  Comet can fly 3 km/s for 37 seconds, but then must rest for 76 seconds.
  Prancer can fly 9 km/s for 12 seconds, but then must rest for 97 seconds.
  Dancer can fly 37 km/s for 1 seconds, but then must rest for 36 seconds.
  """

  @test_content """
  Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
  Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
  """

  def cont() do
    @content
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse/1)
  end

  def cont(_) do
    @test_content
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse/1)
  end

  def solve(testing, seconds) do
    run(testing, seconds)
    |> do_solve(seconds)
  end

  def solve(seconds) do
    run(seconds)
    |> do_solve(seconds)
  end

  def do_solve(run_res, seconds) do
    run_res
    |> Enum.map(fn {x, {y, z}} -> {x, %{"dist" => y, "path" => z}} end)
    |> Enum.into(%{})
    |> score(seconds)
  end

  def score(map, seconds) do
    Enum.map((seconds - 1)..0, fn second -> winners(second, map) end)
  end

  def winners(second, map) do
    scores = Enum.map(map, fn {name, _} -> {name, Map.fetch!(map[name]["path"], second)} end)

    {_, max_score} = Enum.max_by(scores, fn x -> elem(x, 1) end)

    Enum.filter(scores, fn {x, y} -> y == max_score end)
  end

  def run(testing, seconds) when is_integer(seconds) do
    cont(testing)
    |> do_run(seconds)
  end

  def run(seconds) when is_integer(seconds) do
    cont()
    |> do_run(seconds)
  end

  def do_run(z, seconds) do
    z
    |> Enum.map(&run(&1, seconds, 0, 0, 0, %{}))
  end

  # %{"name" => "Vixen", "rest" => 53, "speed" => 8, "speed_t" => 8}
  # seconds, flying, distance
  # finish when no seconds left
  def run(
        %{"name" => name, "rest" => _rest, "speed" => _speed, "speed_t" => _speed_t},
        0,
        _flying,
        distance,
        _resting,
        map
      ) do
    {name, {distance, map}}
  end

  # when rest = resting time then you can continue flying
  def run(
        %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
        seconds,
        speed_t,
        distance,
        rest,
        map
      ) do
    run(
      %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
      seconds,
      0,
      distance,
      0,
      map
    )
  end

  # when flying = speed_t you need to rest for 1 second => no distance increment
  # but lose 1 sec and increase resting
  def run(
        %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
        seconds,
        speed_t,
        distance,
        resting,
        map
      ) do
    s = seconds - 1
    r = resting + 1

    updated_map = Map.put(map, s, distance)

    run(
      %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
      s,
      speed_t,
      distance,
      r,
      updated_map
    )
  end

  # flying
  def run(
        %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
        seconds,
        flying,
        distance,
        r,
        map
      ) do
    distance = distance + speed
    s = seconds - 1
    updated_map = Map.put(map, s, distance)

    run(
      %{"name" => name, "rest" => rest, "speed" => speed, "speed_t" => speed_t},
      seconds - 1,
      flying + 1,
      distance,
      r,
      updated_map
    )
  end

  @re ~r/(?<name>\w+)\s.+\s(?<speed>\d+)\s.+\s(?<speed_t>\d+)\s.+\s(?<rest>\d+)/
  def parse(string) do
    map =
      %{"name" => _name, "speed" => speed, "speed_t" => speed_t, "rest" => rest} =
      Regex.named_captures(@re, string)

    %{
      map
      | "speed" => String.to_integer(speed),
        "speed_t" => String.to_integer(speed_t),
        "rest" => String.to_integer(rest)
    }
  end
end

elem(
  elem(
    Reno.run("test", 1000)
    |> Enum.max_by(&elem(&1, 1)),
    1
  ),
  0
)
|> IO.inspect()

# 2688 => too high
elem(
  elem(
    Reno.run(2503)
    |> Enum.max_by(&elem(&1, 1)),
    1
  ),
  0
)
|> IO.inspect()

# 2655

Reno.solve("test", 1000)
|> List.flatten()
|> Enum.group_by(&elem(&1, 0))
|> Enum.map(fn {x, v} -> {x, length(v)} end)
|> IO.inspect()

Reno.solve(2503)
|> List.flatten()
|> Enum.group_by(&elem(&1, 0))
|> Enum.map(fn {x, v} -> {x, length(v)} end)
|> IO.inspect()
