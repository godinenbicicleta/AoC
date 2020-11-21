defmodule Lights do
  def coords(ux, uy, lx, ly) do
    for x <- lx..ux, y <- ly..uy do
      {x, y}
    end
  end

  def turn_on({x, y}, grid) do
    Map.update(grid, {x, y}, 1, fn _ -> 1 end)
  end

  def turn_off({x, y}, grid) do
    Map.update(grid, {x, y}, 1, fn _ -> 0 end)
  end

  def toggle({x, y}, grid) do
    Map.update(grid, {x, y}, 1, fn
      0 -> 1
      1 -> 0
    end)
  end

  def do_apply(grid, [instruction | rest]) when is_list(instruction) do
    grid
    |> do_apply(instruction)
    |> do_apply(rest)
  end

  def do_apply(grid, ["turn", "on", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &turn_on/2)
  end

  def do_apply(grid, ["turn", "off", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &turn_off/2)
  end

  def do_apply(grid, ["toggle", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &toggle/2)
  end

  def do_apply(grid, []) do
    grid
  end

  def get_instructions do
    File.read!("day6.txt")
    |> Lights.parse()
  end

  def parse(string) do
    string
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&String.split(&1, ~r<[\s,]>))
  end

  def run() do
    %{}
    |> do_apply(get_instructions())
    |> Map.values()
    |> Enum.sum()
  end
end

defmodule Lights2 do
  def coords(ux, uy, lx, ly) do
    for x <- lx..ux, y <- ly..uy do
      {x, y}
    end
  end

  def turn_on({x, y}, grid) do
    Map.update(grid, {x, y}, 1, fn val -> val + 1 end)
  end

  def turn_off({x, y}, grid) do
    Map.update(grid, {x, y}, 0, fn
      0 -> 0
      val -> val - 1
    end)
  end

  def toggle({x, y}, grid) do
    Map.update(grid, {x, y}, 2, fn val -> val + 2 end)
  end

  def do_apply(grid, [instruction | rest]) when is_list(instruction) do
    grid
    |> do_apply(instruction)
    |> do_apply(rest)
  end

  def do_apply(grid, ["turn", "on", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &turn_on/2)
  end

  def do_apply(grid, ["turn", "off", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &turn_off/2)
  end

  def do_apply(grid, ["toggle", upper_x, upper_y, _, lower_x, lower_y]) do
    [ux, uy, lx, ly] = Enum.map([upper_x, upper_y, lower_x, lower_y], &String.to_integer/1)

    coords(ux, uy, lx, ly)
    |> Enum.reduce(grid, &toggle/2)
  end

  def do_apply(grid, []) do
    grid
  end

  def get_instructions do
    File.read!("day6.txt")
    |> Lights.parse()
  end

  def parse(string) do
    string
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&String.split(&1, ~r<[\s,]>))
  end

  def run() do
    %{}
    |> do_apply(get_instructions())
    |> Map.values()
    |> Enum.sum()
  end
end

Lights.run() |> IO.inspect()
Lights2.run() |> IO.inspect()
