defmodule Day20 do
  def main do
    p1()
  end

  def p1 do
    state =
      File.stream!("data/day20.txt")
      |> Enum.map(fn line ->
        line
        |> String.trim()
        |> parse
      end)
      |> Enum.into(%{})

    pulses =
      state["broadcaster"]
      |> elem(2)
      |> Enum.map(fn d -> {:low, d, :broadcaster} end)

    conj_keys =
      state
      |> Enum.filter(fn {_, {t, _, _}} -> t == :conj end)
      |> Enum.map(fn {k, _} -> k end)

    sources_map =
      Enum.map(conj_keys, fn ck ->
        sources =
          state
          |> Enum.filter(fn {_, {_t, _s, dest}} -> ck in dest end)
          |> Enum.map(fn x -> elem(x, 0) end)

        {ck, Enum.map(sources, fn s -> {s, :low} end) |> Enum.into(%{})}
      end)
      |> Enum.into(%{})

    state =
      Enum.reduce(state, %{}, fn
        {key, {type, %{}, dest}}, st ->
          Map.put(st, key, {type, Map.fetch!(sources_map, key), dest})

        {key, m}, st ->
          Map.put(st, key, m)
      end)

    %{low: low, high: high, depth: depth, accs: accs, sts: sts} =
      run_while(pulses, state, state, %{low: 1, high: 0}, 0, [%{}], [state])

    (low * high * div(1000, depth) * div(1000, depth))
    |> IO.inspect()

    {accs, sts}
  end

  def run_while(pulses, state, target, lh, depth, accs = [acc | _rest], sts) do
    depth = depth + 1

    {new_state, %{low: low, high: high}, _, acc} =
      run(pulses, state, lh, depth, acc)

    sts = [new_state | sts]

    accs = [acc | accs]

    if new_state == target or depth == 10000_000 do
      %{low: low, high: high, depth: depth, accs: accs, sts: sts}
    else
      run_while(pulses, new_state, target, %{low: low + 1, high: high}, depth, accs, sts)
    end
  end

  def print_state(state) do
    state
    |> Enum.filter(fn {_k, {_, _, dest}} -> "db" in dest end)
    |> Enum.into(%{})
    |> IO.inspect()
  end

  def resolve_pulse({pulse, to, from}, {state, new_pulses, %{low: low, high: high}, depth, acc}) do
    lowhigh =
      if pulse == :low do
        %{low: low + 1, high: high}
      else
        %{low: low, high: high + 1}
      end

    #     rx = if to == "rx" and pulse == :low, do: rx + 1, else: rx
    if to == "rx" and pulse == :low do
      throw("#{depth}")
    end

    acc = Map.put_new(acc, to, %{low: 0, high: 0})

    acc =
      Map.update(acc, to, nil, fn %{low: low, high: high} ->
        if pulse == :low do
          %{low: low + 1, high: high}
        else
          %{low: low, high: high + 1}
        end
      end)

    # take action on state, 
    if state[to] do
      {type, status, targets} = state[to]

      {new_state, new_pulse} =
        case type do
          :broadcaster ->
            {state, pulse}

          :flipflop ->
            case pulse do
              :high ->
                {state, nil}

              :low ->
                new_status = if status == :off, do: :on, else: :off
                new_state = Map.put(state, to, {type, new_status, targets})

                new_pulse =
                  if status == :off do
                    :high
                  else
                    :low
                  end

                {new_state, new_pulse}
            end

          :conj ->
            # if to == "tg" do
            #  IO.inspect({status, pulse}, label: "old")
            # end

            new_status = Map.put(status, from, pulse)

            # if to == "tg" do
            #  IO.inspect({status, pulse}, label: "new")
            # end

            new_pulse =
              if Enum.all?(new_status, fn {_, v} -> v == :high end) do
                :low
              else
                :high
              end

            new_state = Map.put(state, to, {type, new_status, targets})
            {new_state, new_pulse}
        end

      #
      new_pulses =
        if new_pulse do
          new_pulses ++
            Enum.map(targets, fn target ->
              {new_pulse, target, to}
            end)
        else
          new_pulses
        end

      {new_state, new_pulses, lowhigh, depth, acc}
    else
      {state, new_pulses, lowhigh, depth, acc}
    end
  end

  def run([], state, lowhigh, depth, acc) do
    {state, lowhigh, depth, acc}
  end

  def run(pulses, state, lowhigh, depth, acc) do
    {state, pulses, lowhigh, depth, acc} =
      Enum.reduce(pulses, {state, [], lowhigh, depth, acc}, &resolve_pulse/2)

    run(pulses, state, lowhigh, depth, acc)
  end

  def parse(line) do
    [module, dest] = String.split(line, " -> ")

    dest = dest |> String.split(", ", trim: true)

    [type, state, module] =
      case module do
        "broadcaster" -> [:broadcaster, nil, module]
        "%" <> rest -> [:flipflop, :off, rest]
        "&" <> rest -> [:conj, %{}, rest]
        _ -> [String.to_atom(module), module]
      end

    {module, {type, state, dest}}
  end
end
