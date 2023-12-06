defmodule Day06 do
  def p1 do
    [{56, 546}, {97, 1927}, {78, 1131}, {75, 1139}]
    |> Enum.reduce(1, &(solve(&1) * &2))
  end

  def p2 do
    solve({56_977_875, 546_192_711_311_139})
  end

  def solve({time, record}) do
    s = :math.sqrt(time * time - 4 * record)

    vmax = ((time + s) / 2) |> trunc

    vmin = ((time - s) / 2) |> trunc

    vmax - vmin
  end
end
