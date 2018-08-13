"""Command line interface to SUM Manage commands"""

import click
from summanage.helpers import Helper, LogHelper, Consts
from summanage.sum_commands import SUMCommands
from summanage.alerts_commands import AlertsCommands


@click.command()
@click.option('--command',
              required=True,
              type=click.Choice(['list-sum', 'show-one-sum', 'create-update-sum',
                                 'list-alert-policies', 'show-alert-policy',
                                 'create-sum-alert-condition', 'list-alert-policy-conditions']),
              envvar='COMMAND',
              help='Command to execute')
@click.option('--key',
              required=True,
              envvar='KEY',
              help='New Relic key',
              default='e7d13b66d49c4f1be6209feaa96e70ef')
@click.option('--monitor-name', envvar='MONITORNAME', help='Name of SUM monitor to be managed')
@click.option('--monitor-settings', envvar='MONITORSETTINGS', help='Settings file for SUM monitor')
@click.option('--script-file', envvar='SCRIPTFILE', help='File containing SUM script')
@click.option('--script-injects', envvar='SCRIPTINJECTS', help='Script parameters (to be injected)')
@click.option('--policy-name', envvar='POLICYNAME', help='Name of Alert Policy to be managed')
@click.option('--log-level',
              type=click.Choice(['info', 'debug', 'error']),
              default='info',
              envvar='LOGLEVEL',
              help='Log Level')
def main(command, key, monitor_name, monitor_settings, script_file, script_injects,
         policy_name,
         log_level):
    """CLI interface to NewRelic SUM Commands"""

    # override for testing purposes
    assert key is not None
    consts = Consts(KEY=key)
    helper = Helper()
    logger = LogHelper(log_level)
    sum_commands = SUMCommands(consts, helper, logger)
    alerts_commands = AlertsCommands(consts, helper, logger)

    if command == 'list-sum':
        monitors = sum_commands.get_all_monitors()
        for monitor in monitors:
            logger.info(monitor)

    if command == 'show-one-sum':
        assert monitor_name is not None

        monitor = sum_commands.find_monitor(monitor_name)
        if monitor is not None:
            logger.info('Target monitor: {}'.format(monitor._asdict()))
        else:
            logger.warning('Monitor {} not found'.format(monitor_name))

    if command == 'create-update-sum':
        assert monitor_name is not None
        assert monitor_settings is not None
        assert script_file is not None
        sum_commands.create_update_monitor(monitor_name, monitor_settings,
                                           script_file, script_injects)

    if command == 'list-alert-policies':
        policies = alerts_commands.list_alert_policies()
        for p in policies:
            logger.info(p)

    if command == 'list-alert-policy-conditions':
        #assert monitor_name is not None
        assert policy_name is not None

        policy = alerts_commands.find_alert_policy(policy_name)
        assert policy is not None
        
        conditions = alerts_commands.list_alerts_sum_conditions(policy.id)
        for c in conditions:
            logger.info(c)

    if command == 'show-alert-policy':
        assert policy_name is not None

        policy = alerts_commands.find_alert_policy(policy_name)
        if policy is not None:
            logger.info('Policy found: {}'.format(policy._asdict()))
            sum_conditions = alerts_commands.list_alerts_sum_conditions(
                policy.id)
            logger.info('Policy associated SUM Alert conditions found: {}'
                        .format(len(sum_conditions)))
            logger.info('Policy associated SUM Alert conditions: {}'.format(sum_conditions))
        else:
            logger.warning('Policy {} not found'.format(policy_name))

    if command == 'create-sum-alert-condition':
        #assert monitor_name is not None
        assert policy_name is not None

        policy = alerts_commands.find_alert_policy(policy_name)
        assert policy is not None

        monitor = sum_commands.find_monitor(monitor_name)
        assert monitor is not None

        monitor_id = monitor.id
        monitor_name = monitor.name
        policy_id = policy.id

        alerts_commands.create_update_alerts_sum_condition(
            monitor_id, monitor_name, policy_id)


if __name__ == "__main__":
    main()
